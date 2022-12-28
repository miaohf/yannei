from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Permission, Visit, Contactor, Order, Orderrec
from app.utils.decorator import permission_required
from datetime import datetime


@bp.route('/visits/', methods=['POST'])
@token_auth.login_required
@permission_required(Permission.WRITE)
def create_visit():
    '''添加一篇新拜访日志'''
    data = request.get_json()

    print(data)

    if not data:
        return bad_request('You must post JSON data.')
    message = {}

    if message:
        return bad_request(message)

    now = datetime.now()
    document_code = 'DC' + now.strftime("%Y%m%d%H%M%S")

    visit = Visit()
    visit.from_dict(data)
    visit.author = g.current_user
    visit.document_code = document_code
    visit.visittype_id = 1
    db.session.add(visit)

    contactors = Contactor.query.filter(Contactor.id.in_(data.get('contactorids'))).all()
    for c in contactors:
        visit.contactors.append(c)

    db.session.commit()
    print('commit')
    response = jsonify(visit.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_visit', id=visit.id)
    return response


@bp.route('/visits/', methods=['GET'])
def get_visits():
    '''返回拜访记录集合，分页'''

    print('get_visits')
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    data = Visit.to_collection_dict(
        Visit.query.order_by(Visit.create_at.desc()), page, per_page,
        'api.get_visits')
    return jsonify(data)


@bp.route('/visits/<int:id>', methods=['GET'])
def get_visit(id):
    '''返回一条拜访记录'''
    visit = Visit.query.get_or_404(id)
    data = visit.to_dict()
    return jsonify(data)



@bp.route('/visits/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_visit(id):
    '''修改一篇文章'''
    visit = Visit.query.get_or_404(id)
    if g.current_user != visit.author and not g.current_user.can(Permission.ADMIN):
        return error_response(403)

    data = request.get_json()
    print(data)
    if not data:
        return bad_request('You must post JSON data.')
    message = {}
    # if 'title' not in data or not data.get('title').strip():
    #     message['title'] = 'Title is required.'
    # elif len(data.get('title')) > 255:
    #     message['title'] = 'Title must less than 255 characters.'
    # if 'body' not in data or not data.get('body').strip():
    #     message['body'] = 'Body is required.'
    if message:
        return bad_request(message)

    if data['status_code'] != visit.status_code:
        if data['status_code'] == 1:
            print('提交审核')
            order = Order(document_code = visit.document_code)
            db.session.add(order)
            db.session.flush()
            visit.order_id = order.id
            for node in visit.visittype.workflow.nodes:
                if node not in visit.order.nodes:
                    visit.order.nodes.append(node)
                    orderrec = Orderrec(
                        order_id = order.id,
                        node_id = node.id,
                        team_id = node.team_id)
                    db.session.add(orderrec)
        elif data['status_code'] == 0:
            visit.order.status_code = 3
            for orderrec in visit.order.orderrecs:
                orderrec.status_code = 9


    visit.from_dict(data)
    db.session.commit()
    return jsonify(visit.to_dict())


@bp.route('/visits/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_visit(id):
    '''删除一篇文章'''
    visit = Visit.query.get_or_404(id)
    if g.current_user != visit.author and not g.current_user.can(Permission.ADMIN):
        return error_response(403)
    db.session.delete(visit)
    db.session.commit()
    return '', 204


# ###
# # 与博客文章资源相关的资源
# ##
# @bp.route('/visits/<int:id>/comments/', methods=['GET'])
# def get_post_comments(id):
#     '''返回当前文章下面的一级评论'''
#     post = Post.query.get_or_404(id)
#     page = request.args.get('page', 1, type=int)
#     per_page = min(
#         request.args.get(
#             'per_page', current_app.config['COMMENTS_PER_PAGE'], type=int), 100)
#     # 先获取一级评论
#     data = Comment.to_collection_dict(
#         post.comments.filter(Comment.parent==None).order_by(Comment.timestamp.desc()), page, per_page,
#         'api.get_post_comments', id=id)
#     # 再添加子孙到一级评论的 descendants 属性上
#     for item in data['items']:
#         comment = Comment.query.get(item['id'])
#         descendants = [child.to_dict() for child in comment.get_descendants()]
#         # 按 timestamp 排序一个字典列表
#         from operator import itemgetter
#         item['descendants'] = sorted(descendants, key=itemgetter('timestamp'))
#     return jsonify(data)


# ###
# # 文章被喜欢/收藏 或 被取消喜欢/取消收藏
# ###
# @bp.route('/visits/<int:id>/like', methods=['GET'])
# @token_auth.login_required
# def like_post(id):
#     '''喜欢文章'''
#     post = Post.query.get_or_404(id)
#     post.liked_by(g.current_user)
#     db.session.add(post)
#     # 切记要先提交，先添加喜欢记录到数据库，因为 new_posts_likes() 会查询 posts_likes 关联表
#     db.session.commit()
#     # 给文章作者发送新喜欢通知
#     post.author.add_notification('unread_posts_likes_count',
#                                  post.author.new_posts_likes())
#     db.session.commit()
#     return jsonify({
#         'status': 'success',
#         'message': 'You are now liking this post.'
#     })


# @bp.route('/visits/<int:id>/unlike', methods=['GET'])
# @token_auth.login_required
# def unlike_post(id):
#     '''取消喜欢文章'''
#     post = Post.query.get_or_404(id)
#     post.unliked_by(g.current_user)
#     db.session.add(post)
#     # 切记要先提交，先添加喜欢记录到数据库，因为 new_posts_likes() 会查询 posts_likes 关联表
#     db.session.commit()
#     # 给文章作者发送新喜欢通知(需要自动减1)
#     post.author.add_notification('unread_posts_likes_count',
#                                  post.author.new_posts_likes())
#     db.session.commit()
#     return jsonify({
#         'status': 'success',
#         'message': 'You are not liking this post anymore.'
#     })


# @bp.route('/visits/export-posts/', methods=['GET'])
# @token_auth.login_required
# @permission_required(Permission.WRITE)
# def export_posts():
#     '''导出当前用户的所有文章，RQ 后台任务'''
#     if g.current_user.get_task_in_progress('export_posts'):  # 如果用户已经有同名的后台任务在运行中时
#         return bad_request('上一个导出文章的后台任务尚未结束')
#     else:
#         # 将 app.utils.tasks.export_posts 放入任务队列中
#         g.current_user.launch_task('export_posts', '正在导出文章...', kwargs={'user_id': g.current_user.id})
#         return jsonify(message='正在运行导出文章后台任务')

