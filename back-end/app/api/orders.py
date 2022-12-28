from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Permission, Order
from app.utils.decorator import permission_required



@bp.route('/orders/', methods=['GET'])
def get_orders():
    '''返回审批记录集合，分页'''

    print('get_orders')
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)

    print('to_collection_dict')
    data = Order.to_collection_dict(
        Order.query.filter(Order.status_code != 3).order_by(Order.create_at.desc()), page, per_page,
        'api.get_orders')
    return jsonify(data)


@bp.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    '''返回一条审批记录'''
    order = Order.query.get_or_404(id)
    data = order.to_dict()

    return jsonify(data)



