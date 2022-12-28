from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Permission, Customer, Contactor, Address
from app.utils.decorator import permission_required


@bp.route('/customers/', methods=['POST'])
@token_auth.login_required
@permission_required(Permission.WRITE)
def create_customer():
    '''添加一个客户档案'''
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    message = {}
    # if 'title' not in data or not data.get('title').strip():
    #     message['title'] = 'Title is required.'

    if message:
        return bad_request(message)

    customer = Customer()
    customer.from_dict(data)
    # customer.author = g.current_user  # 通过 auth.py 中 verify_token() 传递过来的（同一个request中，需要先进行 Token 认证）
    db.session.add(customer)

    db.session.commit()
    response = jsonify(customer.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_customer', id=customer.id)
    return response


@bp.route('/customers/', methods=['GET'])
def get_customers():
    '''返回拜访记录集合，分页'''

    print('get_customers')
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)

    print('to_collection_dict')
    data = Customer.to_collection_dict(
        Customer.query.order_by(Customer.create_at.desc()), page, per_page,
        'api.get_customers')
    return jsonify(data)


@bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    '''返回一条拜访记录'''
    customer = Customer.query.get_or_404(id)
    data = customer.to_dict()
    return jsonify(data)


@bp.route('/customers/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_customer(id):
    '''修改一个客户档案'''
    customer = Customer.query.get_or_404(id)
    # if not g.current_user.can(Permission.ADMIN):
    #     return error_response(403)

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    message = {}

    if message:
        return bad_request(message)

    customer.from_dict(data)
    db.session.commit()
    return jsonify(customer.to_dict())


@bp.route('/customers/<int:id>', methods=['POST'])
@token_auth.login_required
def add_contactor_or_address_by_customer(id):
    '''修改客户档案，新增联系人'''
    customer = Customer.query.get_or_404(id)

    data = request.get_json()
    print(data)

    if not data:
        return bad_request('You must post JSON data.')
    message = {}

    if message:
        return bad_request(message)

    if data.get('type') == 'contactor':
        print('add contactor')
        model = Contactor()
    elif data.get('type') == 'address':
        print('add address')
        model = Address()
    else:
        print('type not found')

    model.from_dict(data)
    # customer.contactors.append(contactor)
    model.customer = customer
    db.session.add(model)
    db.session.commit()
    return jsonify(customer.to_dict())



@bp.route('/customers/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_customer(id):
    '''删除一个客户档案'''
    customer = Customer.query.get_or_404(id)
    if not g.current_user.can(Permission.ADMIN) > 0:
        return error_response(403)
    db.session.delete(customer)
    db.session.commit()
    return '', 204

