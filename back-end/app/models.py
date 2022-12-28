import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
import jwt
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for, current_app
from app.extensions import db
from app.utils.elasticsearch import add_to_index, remove_from_index, query_index, es_highlight
from sqlalchemy_serializer import SerializerMixin


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # 如果当前没有任何资源时，或者前端请求的 page 越界时，都会抛出 404 错误
        # 由 @bp.app_errorhandler(404) 自动处理，即响应 JSON 数据：{ error: "Not Found" }
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data




class Permission:
    '''权限认证中的各种操作，对应二进制的位，比如
    FOLLOW: 0b00000001，转换为十六进制为 0x01
    COMMENT: 0b00000010，转换为十六进制为 0x02
    WRITE: 0b00000100，转换为十六进制为 0x04
    ...
    ADMIN: 0b10000000，转换为十六进制为 0x80

    中间还预留了第 4、5、6、7 共4位二进制位，以备后续增加操作权限
    '''
    # 关注其它用户的权限
    FOLLOW = 0x01
    # 发表评论、评论点赞与踩的权限
    COMMENT = 0x02
    # 撰写文章的权限
    WRITE = 0x04
    # 管理网站的权限(对应管理员角色)
    ADMIN = 0x80


class Role(db.Model, PaginatedAPIMixin, SerializerMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))  # 角色名称
    default = db.Column(db.Boolean, default=False, index=True)  # 当新增用户时，是否将当前角色作为默认角色赋予新用户
    permissions = db.Column(db.Integer)  # 角色拥有的权限，各操作对应一个二进制位，能执行某项操作的角色，其位会被设为 1
    users = db.relationship('User', backref='role', lazy='dynamic')
    # users = db.relationship('Users', secondary=users_roles, backref=db.backref('roles'))

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        '''应用部署时，应该主动执行此函数，添加以下角色
        shutup:        0b0000 0000 (0x00) 收回所有权限
        reader:        0b0000 0011 (0x03) 可读
        author:        0b0000 0111 (0x07) 可读可写
        administrator: 0b1000 0111 (0x87) 超级管理员，拥有全部权限

        以后如果要想添加新角色，或者修改角色的权限，修改 roles 数组，再运行函数即可
        '''
        roles = {
            'shutup': ('无权限', ()),
            'reader': ('读者', (Permission.FOLLOW, Permission.COMMENT)),
            'author': ('作者', (Permission.FOLLOW, Permission.COMMENT, Permission.WRITE)),
            'administrator': ('管理员', (Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.ADMIN)),
        }
        default_role = 'reader'
        for r in roles:  # r 是字典的键
            role = Role.query.filter_by(slug=r).first()
            if role is None:
                role = Role(slug=r, name=roles[r][0])
            role.reset_permissions()
            for perm in roles[r][1]:
                role.add_permission(perm)
            role.default = (role.slug == default_role)
            db.session.add(role)
        db.session.commit()

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def get_permissions(self):
        '''获取角色的具体操作权限列表'''
        p = [(Permission.FOLLOW, 'follow'), (Permission.COMMENT, 'comment'), (Permission.WRITE, 'write'), (Permission.ADMIN, 'admin')]
        new_p = filter(lambda x: self.has_permission(x[0]), p)
        return ','.join([x[1] for x in new_p])  # 用逗号拼接成str

    def to_dict(self):
        data = {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'default': self.default,
            'permissions': self.permissions,
            '_links': {
                'self': url_for('api.get_role', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['slug', 'name', 'permissions']:
            if field in data:
                setattr(self, field, data[field])

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Role {}>'.format(self.name)

users_teams = db.Table(
    'users_teams',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id')),
    db.PrimaryKeyConstraint('user_id', 'team_id'),
)


class User(db.Model, PaginatedAPIMixin, SerializerMixin):
    # 设置数据库表名，Post模型中的外键 user_id 会引用 users.id
    __tablename__ = 'users'
    serialize_rules = ("-role.users", "-orderrecs", )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 不保存原始密码
    name = db.Column(db.String(64))
    status_code = db.Column(db.Integer, default=0) # 0  正常     
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)

    # 用户的通知
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic', cascade='all, delete-orphan')
    
    # 用户最后一次查看私信的时间
    last_messages_read_time = db.Column(db.DateTime)
   
    # 用户注册后，需要先确认邮箱
    confirmed = db.Column(db.Boolean, default=False)
    # 用户所属的角色
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # 用户的RQ后台任务
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    # 拜访日志
    visits = db.relationship('Visit', backref='author', lazy='dynamic')

    # 审批记录
    orderrecs = db.relationship('Orderrec', backref='auditor', lazy='dynamic')


    @staticmethod
    def init_data():
        users = [
        {'name': '张三', 'team_id': 1, 'username': 'zhangsan'}, 
        {'name': '李四', 'team_id': 1, 'username': 'lisi'}, 
        {'name': '王五', 'team_id': 1, 'username': 'wangwu'}, 
        {'name': '赵六', 'team_id': 2, 'username': 'zhaoliu'}, 
        {'name': '曹操', 'team_id': 2, 'username': 'caochao'}, 
        {'name': '关羽', 'team_id': 2, 'username': 'guanyu'}
        ]

        for u in users:  
            t = Team.query.get(u['team_id'])
            user = User(
                name=u['name'],
                username=u['username'],
                email=u['username'] + '@yanei.com',
                )                

            t.users.append(user)
            db.session.add(user)
        db.session.commit()


    def set_password(self, password):
        '''设置用户密码，保存为 Hash 值'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''验证密码与保存的 Hash 值是否匹配'''
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        '''用户头像'''
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'name', 'location', 'about_me', 'confirmed', 'role_id']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
            # 新建用户时，给用户自动分配角色
            if self.role is None:
                if self.email in current_app.config['ADMINS']:
                    self.role = Role.query.filter_by(slug='administrator').first()
                else:
                    self.role = Role.query.filter_by(default=True).first()

    def ping(self):
        '''更新用户的最后访问时间'''
        self.last_seen = datetime.now()
        db.session.add(self)

    def get_jwt(self, expires_in=36000):
        '''用户登录后，发放有效的 JWT'''
        now = datetime.now()
        payload = {
            'user_id': self.id,
            'confirmed': self.confirmed,
            'user_name': self.name if self.name else self.username,
            'user_avatar': base64.b64encode(self.avatar(24).
                                            encode('utf-8')).decode('utf-8'),
            'permissions': self.role.get_permissions(),
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        '''验证 JWT 的有效性'''
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.DecodeError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return None
        return User.query.get(payload.get('user_id'))


    def add_notification(self, name, data):
        '''给用户实例对象增加通知'''
        # 如果具有相同名称的通知已存在，则先删除该通知
        self.notifications.filter_by(name=name).delete()
        # 为用户添加通知，写入数据库
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def new_received_messages(self):
        '''用户未读的私信计数'''
        last_read_time = self.last_messages_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def generate_confirm_jwt(self, expires_in=3600):
        '''生成确认账户的 JWT'''
        now = datetime.now()
        payload = {
            'confirm': self.id,
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    def verify_confirm_jwt(self, token):
        '''用户点击确认邮件中的URL后，需要检验 JWT，如果检验通过，则把新添加的 confirmed 属性设为 True'''
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.DecodeError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return False
        if payload.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_password_jwt(self, expires_in=3600):
        '''生成重置账户密码的 JWT'''
        now = datetime.now()
        payload = {
            'reset_password': self.id,
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_jwt(token):
        '''用户点击重置密码邮件中的URL后，需要检验 JWT
        如果检验通过，则返回 JWT 中存储的 id 所对应的用户实例'''
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.DecodeError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return None
        return User.query.get(payload.get('reset_password'))

    def can(self, perm):
        '''检查用户是否有指定的权限'''
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        '''检查用户是否为管理员'''
        return self.can(Permission.ADMIN)

    def get_task_in_progress(self, name):
        '''检查指定任务名的RQ任务是否还在运行中'''
        return Task.query.filter_by(name=name, user=self, complete=False).first()

    def launch_task(self, name, description, *args, **kwargs):
        '''用户启动一个新的后台任务'''
        rq_job = current_app.task_queue.enqueue('app.utils.tasks.' + name, *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name, description=description, user=self)
        db.session.add(task)
        db.session.commit()
        return task

    def get_tasks_in_progress(self):
        '''返回用户所有正在运行中的后台任务'''
        return Task.query.filter_by(user=self, complete=False).all()




    def __repr__(self):
        return '<User {}>'.format(self.username)



class Notification(db.Model):  # 不需要分页
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def __repr__(self):
        return '<Notification {}>'.format(self.id)

    def get_data(self):
        return json.loads(str(self.payload_json))


    def from_dict(self, data):
        for field in ['body', 'timestamp']:
            if field in data:
                setattr(self, field, data[field])


class Message(db.Model, PaginatedAPIMixin, SerializerMixin):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Message {}>'.format(self.id)

    def from_dict(self, data):
        for field in ['body', 'timestamp']:
            if field in data:
                setattr(self, field, data[field])


class Task(db.Model, PaginatedAPIMixin, SerializerMixin):
    __tablename__ = 'tasks'
    # 不使用默认的整数主键，而是用 RQ 为每个任务生成的字符串ID
    id = db.Column(db.String(36), primary_key=True)
    # 任务名
    name = db.Column(db.String(128), index=True)
    # 任务描述
    description = db.Column(db.String(128))
    # 任务所属的用户
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 是否已执行完成
    complete = db.Column(db.Boolean, default=False)

    def get_progress(self):
        '''返回Task对象实时的进度'''
        try:
            # 通过Task.id，返回RQ job实例
            rq_job = current_app.task_queue.fetch_job(self.id)
        except Exception:
            rq_job = None
        return rq_job.meta.get('progress', 0) if rq_job is not None else 100


    def __repr__(self):
        return '<Task {}>'.format(self.id)



users_customers = db.Table(
    'users_customers',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('customer_id', db.Integer, db.ForeignKey('customers.id')),
    db.PrimaryKeyConstraint('user_id', 'customer_id'),
)



# 客户表(是指公司或者单位)
class Customer(db.Model, PaginatedAPIMixin, SerializerMixin):
    __tablename__ = 'customers'
    serialize_rules = ("-city.customers", "-contactor.customers", "-visits", )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(128))
    phone = db.Column(db.String(12))
    description = db.Column(db.String(128), default='')
    create_at = db.Column(db.DateTime(), default=datetime.now)
    last_update = db.Column(db.DateTime(), onupdate=datetime.now, default=datetime.now)

    contactors = db.relationship('Contactor', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    addresses = db.relationship('Address', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    visits = db.relationship('Visit', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    users = db.relationship('User', secondary=users_customers, backref=db.backref('customers'))


    def from_dict(self, data):
        for field in ['name', 'address', 'phone', 'description', 'province_id', 'city_id']:
            if field in data:
                setattr(self, field, data[field])


    @staticmethod
    def init_data():
        customers = [
            {'name': '杭州研一智控科技有限公司', 'phone': '057186800286', 'address': '杭州市钱塘新区下沙23号大街505号B座5楼', 
            'description': '杭州研一智控科技有限公司成立于2016年，位于浙江省杭州市钱塘区，是一家集研发、生产、销售和服务于一体的国家高新技术企业。研一智控致力于智慧实验 室建设，\
            借助物联网、云计算、大数据、智能化控制和移动互联等信息技术实现数据驱动下的智能化实验室建设。研一智控作为实验室智能管理的引领者，基于现有的成熟产品以及对该业务领域的深刻\
            理解，研发团队从智能物资管理入手，率先引入智能化管理、RFID无线 射频等理念与技术，探索和研发智能化管理系统及智能化硬件设备，通过软硬件一体的管理方式实现硬件自我诊断、故\
            障报告及数据的自动解析和处理等，以 及化学试剂等物资的全生命周期管理，将人、物、境相连并进行统筹管理，为实验室的管理提供资源高度可控、统一协调的智慧服务。经过研发团队不断\
            探索和钻研的努力下研一智控在智能管理理念、技术革新、系统集成等多方面创下行业先例，用户覆盖全国所有的直辖市、80%以上副省级 城市及50+其它重要城市，满足300+机关/事业单位、\
            科研院所、高校、企业等不同领域的共性需求与个性化定制管理需求需求和应用场景，以信息化、智能化 的理念为用户创造非凡业绩与持久价值。', 'province_id': 1, 'city_id': 1},
            {'name': '华为技术有限公司', 'phone': '4008229999', 'address': '深圳市龙岗区坂田街道', 
            'description': '华为创立于1987年，是全球领先的ICT（信息与通信）基础设施和智能终端提供商。目前华为约有19.5万员工，业务遍及170多个国家和地区，服务全球30多亿人口。华为\
            致力于把数字世界带入每个人、每个家庭、每个组织，构建万物互联的智能世界：让无处不在的联接，成为人人平等的权利，成为智能世界的前提和基础；为世界提供多样性算力，让云无处不\
            在，让智能无所不及；所有的行业和组织，因强大的数字平台而变得敏捷、高效、生机勃勃；通过AI重新定义体验，让消费者在家居、出行、办公、影音娱乐、运动健康等全场景获得极致的个性化\
            智慧体验。', 'province_id': 6, 'city_id': 8},
            {'name': '腾讯控股有限公司', 'phone': '4009100100', 'address': '深圳市南山區海天二路33號騰訊濱海大廈', 
            'description': '腾讯是一家世界领先的互联网科技公司，用创新的产品和服务提升全球各地人们的生活品质。腾讯成立于1998年，总部位于中国深圳。公司一直秉承科技向善的宗旨。我们\
            的通信和社交服务连接全球逾10亿人，帮助他们与亲友联系，畅享便捷的出行、支付和娱乐生活。腾讯发行多款风靡全球的电子游戏及其他优质数字内容，为全球用户带来丰富的互动娱乐体验。\
            腾讯还提供云计算、广告、金融科技等一系列企业服务，支持合作伙伴实现数字化转型，促进业务发展。腾讯2004 年于香港联合交易所上市。', 'province_id': 6, 'city_id': 8}
        
        ]

        for c in customers:  
            customer = Customer(
                name=c['name'],
                phone=c['phone'],
                address=c['address'],
                description=c['description'],
                # province_id=c['province_id'],
                # city_id=c['city_id'],
                )
            db.session.add(customer)
        db.session.commit()


    def __repr__(self):
        return '<Customer {}>'.format(self.id)



# 客户联系人表
class Address(db.Model, SerializerMixin):
    __tablename__ = 'addresses'
    serialize_rules = ("-customer", "-visits", )

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(20))
    address_info = db.Column(db.String(50))
    description = db.Column(db.String(128))
    create_at = db.Column(db.DateTime(), default=datetime.now)
    last_update = db.Column(db.DateTime(), onupdate=datetime.now, default=datetime.now)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))

    visits = db.relationship('Visit', backref='address', lazy='dynamic')


    def from_dict(self, data):
        for field in ['department', 'address', 'description', 'province_id', 'city_id']:
            if field in data:
                setattr(self, field, data[field])


    @staticmethod
    def init_data():
        addresses = [
        {'department': '总部', 'address_info': '杭州市钱塘新区下沙23号大街505号B座5楼', 'description': '研一智控公司总部', 'province_id': 1, 'city_id': 1, 'customer_id': 1},
        {'department': '第一分公司', 'address_info': '广州市番禺区东环街东沙村汪坡三街北六巷3号', 'description': '研一智控第一分公司', 'province_id': 6, 'city_id': 7, 'customer_id': 1},
        {'department': '总部', 'address_info': '深圳市龙岗区坂田街道', 'description': '华为技术公司总部', 'province_id': 6, 'city_id': 8, 'customer_id': 2},
        {'department': '总部', 'address_info': '深圳市南山區海天二路33號騰訊濱海大廈', 'description': '腾讯控股公司总部', 'province_id': 6, 'city_id': 8, 'customer_id': 3},

        ]
        for addr in addresses:
            address = Address(
                department=addr['department'],
                address_info=addr['address_info'],
                description=addr['description'],
                province_id=addr['province_id'],
                city_id=addr['city_id'],
                customer_id=addr['customer_id'],
                )
            db.session.add(address)
        db.session.commit()


    def __repr__(self):
        return '<Address {}>'.format(self.id)



contactors_visits = db.Table(
    'contactors_visits',
    db.Column('contactor_id', db.Integer, db.ForeignKey('contactors.id')),
    db.Column('visit_id', db.Integer, db.ForeignKey('visits.id')),
    db.PrimaryKeyConstraint('contactor_id', 'visit_id'),
)



# 客户联系人表
class Contactor(db.Model, SerializerMixin):
    __tablename__ = 'contactors'
    serialize_rules = ("-customer", "-visits",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    mobile = db.Column(db.String(11))
    position = db.Column(db.String(30))
    description = db.Column(db.String(128))

    # add by 20220616
    age = db.Column(db.Integer)
    sex = db.Column(db.String(1))                   #0男 1女
    ismarried = db.Column(db.String(1))             #0未婚 1已婚
    email = db.Column(db.String(30))
    phone = db.Column(db.String(12))
    wechatid = db.Column(db.String(30))
    office_address = db.Column(db.String(30))
    education_level = db.Column(db.String(1))       #1高中 2中专 3大专 4本科 5硕士 6博士 7教授
    graduated_school = db.Column(db.String(50))
    spouse_detail = db.Column(db.String(200))
    child_detail = db.Column(db.String(200))

    create_at = db.Column(db.DateTime(), default=datetime.now)
    last_update = db.Column(db.DateTime(), onupdate=datetime.now, default=datetime.now)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    visits = db.relationship('Visit', backref='contactor', lazy='dynamic')

    visits = db.relationship('Visit', secondary=contactors_visits, backref=db.backref('contactors'))



    def from_dict(self, data):
        for field in ['name', 'mobile', 'position', 'description', 'sex', 'age', 'email', 'phone', 'office_address', \
        'wechatid',  'graduated_school', 'spouse_detail', 'child_detail', 'customer_id']:
            if field in data:
                setattr(self, field, data[field])


    @staticmethod
    def init_data():
        contactors = [
        {'name': '海峰', 'mobile': 13858003606, 'position': '软件开发工程师', 'description': '嘿嘿', 'customer_id': 1},
        {'name': '关羽', 'mobile': 13000000001, 'position': '蜀中大将', 'description': '嘿嘿', 'customer_id': 1},
        {'name': '悟空', 'mobile': 13900000002, 'position': '美猴王', 'description': '你猜猜', 'customer_id': 1},
        {'name': '沙僧', 'mobile': 18600000001, 'position': '沙河之王', 'description': '你猜猜', 'customer_id': 1},
        {'name': '虞美人', 'mobile': 18600000002, 'position': '天下最美', 'description': '你猜猜', 'customer_id': 1},
        {'name': '曹操', 'mobile': 18600000003, 'position': '说曹操曹操就到', 'description': '你猜猜', 'customer_id': 1},
        {'name': '刘皇叔', 'mobile': 18600000004, 'position': '就是刘备嘛', 'description': '你猜猜', 'customer_id': 1},
        {'name': '孔子', 'mobile': 18600000005, 'position': '孔夫子孔圣人', 'description': '你猜猜', 'customer_id': 1},
        {'name': '观音菩萨', 'mobile': 18600000006, 'position': '小小菩萨', 'description': '你猜猜', 'customer_id': 1},
        {'name': '项羽', 'mobile': 18600000007, 'position': '力拔山兮', 'description': '你猜猜', 'customer_id': 1},




        {'name': '任正非', 'mobile': 13900000003, 'position': '反美斗士', 'description': '你猜猜', 'customer_id': 2},
        {'name': '马化腾', 'mobile': 13900000004, 'position': '企鹅之父', 'description': '你猜猜', 'customer_id': 3},
        ]
        for c in contactors:  
            contactor = Contactor(
                name=c['name'],
                mobile=c['mobile'],
                position=c['position'],
                customer_id=c['customer_id'],
                )
            db.session.add(contactor)
        db.session.commit()


    def __repr__(self):
        return '<Contactor {}>'.format(self.id)
        


# 拜访记录表
class Visit(db.Model, PaginatedAPIMixin, SerializerMixin):
    __tablename__ = 'visits'
    serialize_rules = ("-author.roles", "-author.visits", "-customer",  "-visittype", "-order.visit", "customer_name",  "contactorids", )

    id = db.Column(db.Integer, primary_key=True)
    document_code = db.Column(db.String(100))           # DC202205310001
    title = db.Column(db.String(60))
    description = db.Column(db.String(512))
    status_code = db.Column(db.Integer, default=0)      # 0新建  1审核中 2完成 9驳回
    create_at = db.Column(db.DateTime(), default=datetime.now)
    last_update = db.Column(db.DateTime(), onupdate=datetime.now, default=datetime.now)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    # contactor_id = db.Column(db.Integer, db.ForeignKey('contactors.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    visittype_id = db.Column(db.Integer, db.ForeignKey('visittypes.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))


    attachments = db.relationship('Attachment', backref='visit', lazy='dynamic')

    

    def customer_name(self):
        return self.customer.name


    def author_name(self):
        return self.author.name

    def contactorids(self):
        return [contactor.id for contactor in self.contactors]


    def __repr__(self):
        return '<Visit {}>'.format(self.id)

    def from_dict(self, data):
        # for field in ['title', 'description', 'customer_id', 'contactor_id', 'visittype_id', 'author_id', 'address_id', 'status_code']:
        for field in ['title', 'description', 'customer_id', 'contactor_id', 'author_id', 'address_id', 'status_code']:
            if field in data:
                setattr(self, field, data[field])



# 附件表
class Attachment(db.Model, SerializerMixin):
    __tablename__ = 'attachments'
    serialize_rules = ("-visit", )

    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(100))
    type_code = db.Column(db.String(1))                 # 0现场照片 1客户签字
    create_at = db.Column(db.DateTime(), default=datetime.now)
    last_update = db.Column(db.DateTime(), onupdate=datetime.now, default=datetime.now)

    visit_id = db.Column(db.Integer, db.ForeignKey('visits.id'))


    def __repr__(self):
        return '<Attachment {}>'.format(self.id)



# 拜访类型表
class Visittype(db.Model, SerializerMixin):
    __tablename__ = 'visittypes'
    serialize_rules = ("-visits",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type_code = db.Column(db.String(1))                 # 0销售拜访 1售后服务
    create_at = db.Column(db.DateTime(), default=datetime.now)
    last_update = db.Column(db.DateTime(), onupdate=datetime.now, default=datetime.now)

    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'))

    visits = db.relationship('Visit', backref='visittype', lazy='dynamic')


    @staticmethod
    def init_data():
        visittypes = [
        {'name': '销售拜访1个审批节点', 'workflow_id': 1},
        {'name': '销售拜访2个审批节点', 'workflow_id': 2},
        {'name': '售后服务2个审批节点', 'workflow_id': 3}
        ]
        for v in visittypes:  
            visittype = Visittype(
                name=v['name'],
                workflow_id=v['workflow_id']
                )
            db.session.add(visittype)
        db.session.commit()


    def __repr__(self):
        return '<Visittype {},{}>'.format(self.id, self.name)


orders_nodes = db.Table(
    'orders_nodes',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    db.Column('node_id', db.Integer, db.ForeignKey('nodes.id')),
    db.PrimaryKeyConstraint('order_id', 'node_id'),
)



# 工作流配置表
class Workflow(db.Model, SerializerMixin):
    __tablename__ = 'workflows'
    serialize_rules = ("-visittypes", )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    status_code = db.Column(db.Integer, default=0)      # 0启用  1不启用        
    create_at = db.Column(db.DateTime(), default=datetime.now)
    last_update = db.Column(db.DateTime(), onupdate=datetime.now, default=datetime.now)

    visittypes = db.relationship('Visittype', backref='workflow', lazy='dynamic')
    nodes = db.relationship('Node', backref='workflow', lazy='dynamic')


    @staticmethod
    def init_data():
        workflows = ['workflow01', 'workflow02', 'workflow03']
        for wf in workflows:  
            workflow = Workflow(name=wf)
            db.session.add(workflow)
        db.session.commit()


    def __repr__(self):
        return '<Workflow {}, {}>'.format(self.id, self.name)



# 工作流节点配置表
class Node(db.Model, SerializerMixin):
    __tablename__ = 'nodes'
    serialize_rules = ("-workflow", "-orderrecs", )

    id = db.Column(db.Integer, primary_key=True)
    nodename = db.Column(db.String(15))
    status_code = db.Column(db.Integer, default=0)      # 0启用  1不启用
    create_at = db.Column(db.DateTime(), default=datetime.now)
    last_update = db.Column(db.DateTime(), onupdate=datetime.now, default=datetime.now)

    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    orderrecs = db.relationship('Orderrec', backref='node', lazy='dynamic')


    @staticmethod
    def init_data():
        nodes = [
        ['node01', 1, 1],

        ['node11', 2, 1],
        ['node12', 2, 2],

        ['node21', 3, 3],
        ['node22', 3, 4],
        ['node23', 3, 5],
        ]

        for n in nodes:  
            node = Node(nodename=n[0], workflow_id=n[1], team_id=n[2])
            db.session.add(node)
        db.session.commit()

    def __repr__(self):
        return '<Node {}>'.format(self.id)



# 审计组配置
class Team(db.Model, SerializerMixin):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    serialize_rules = ("-users", "-orderrecs", "team_member",)

    name = db.Column(db.String(15))   
    create_at = db.Column(db.DateTime(), default=datetime.now)
    last_update = db.Column(db.DateTime(), onupdate=datetime.now, default=datetime.now)

    # node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))

    users = db.relationship('User', secondary=users_teams, backref=db.backref('teams'))
    orderrecs = db.relationship('Orderrec', backref='team', lazy='dynamic')

    @staticmethod
    def init_data():
        teams = ['team1001', 'team1002', 'team2001', 'team2002']
        for t in teams:  
            team = Team(name=t)
            db.session.add(team)
        db.session.commit()

    def team_member(self):
        data =  [{'id': u.id, 'name': u.name, 'username': u.username} for u in self.users]
        return data

    def __repr__(self):
        return '<Team {}>'.format(self.id)



# 审批工单表
class Order(db.Model, PaginatedAPIMixin, SerializerMixin):
    __tablename__ = 'orders'
    serialize_only = ("id", "document_code", "status_code", "create_at", "last_update", "orderrecs", "visit")
    # serialize_only = ("id", "document_code", "status_code", "create_at", "last_update", "visit")
    # serialize_rules = ("-visit.order", "-nodes.order", )

    id = db.Column(db.Integer, primary_key=True)
    document_code = db.Column(db.String(100))           # GD202205310001
    status_code = db.Column(db.Integer, default=0)      # 0未审 1送审 3审核通过 9驳回
    create_at = db.Column(db.DateTime(), default=datetime.now)
    last_update = db.Column(db.DateTime(), onupdate=datetime.now, default=datetime.now)

    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'))

    orderrecs = db.relationship('Orderrec', backref=db.backref('order'))

    nodes = db.relationship('Node', secondary=orders_nodes, backref=db.backref('orders'))
    visit = db.relationship('Visit', backref='order', uselist=False)

    def __repr__(self):
        return '<Order {}>'.format(self.id)




# 审批记录表
class Orderrec(db.Model, SerializerMixin):
    __tablename__ = 'orderrecs'
    serialize_rules = ("-order", "-node", "-auditor.visits", "nodename", )

    id = db.Column(db.Integer, primary_key=True)
    status_code = db.Column(db.Integer, default=0)      # 0未审 3审核通过 9驳回
    opinion_text = db.Column(db.String(200)) 
    create_at = db.Column(db.DateTime(), default=datetime.now)
    last_update = db.Column(db.DateTime(), onupdate=datetime.now, default=datetime.now)

    auditor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))

    def nodename(self):
        return self.node.nodename

    def from_dict(self, data):
        for field in ['status_code', 'opinion_text']:
            if field in data:
                setattr(self, field, data[field])


    def __repr__(self):
        return '<Orderrec {}>'.format(self.id)



# 省份表
class Province(db.Model, SerializerMixin):
    __tablename__ = 'provinces'
    serialize_rules = ("-addresses", )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    create_at = db.Column(db.DateTime(), default=datetime.now)

    cities = db.relationship('City', backref='province', lazy='dynamic')
    addresses = db.relationship('Address', backref='province', lazy='dynamic')


    @staticmethod
    def init_data():
        provinces = ['浙江', '福建', '江苏', '江西', '安徽', '广东', '云南', '四川']

        for province_name in provinces:  
            province = Province(name=province_name)
            db.session.add(province)
        db.session.commit()

    def __repr__(self):
        return '<Province {}>'.format(self.id)



# 地市表
class City(db.Model, SerializerMixin):
    __tablename__ = 'cities'
    serialize_rules = ("-province.cities", "-addresses",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    city_code = db.Column(db.String(4))
    create_at = db.Column(db.DateTime(), default=datetime.now)

    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'))
    addresses = db.relationship('Address', backref='city', lazy='dynamic')

    # customers = db.relationship('Customer', backref='city', lazy='dynamic')

    @staticmethod
    def init_data():
        citis = [
            ['杭州', '0571', 1],
            ['福州', '0591', 2],
            ['厦门', '0592', 2],
            ['南京', '025', 3],
            ['南昌', '0791', 4],
            ['芜湖', '0553', 5],
            ['广州', '020', 6],
            ['深圳', '0755', 6],
            ['昆明', '0871', 7],
            ['成都', '028', 8],
            ['广州', '020', 6],
        ]

        for c in citis:  
            city = City(name=c[0], city_code=c[1], province_id=c[2])
            db.session.add(city)
        db.session.commit()

    def __repr__(self):
        return '<City {}>'.format(self.id)
