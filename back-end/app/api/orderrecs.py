from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Permission, Orderrec
from app.utils.decorator import permission_required





@bp.route('/orderrecs/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_orderrec(id):
    '''审批记录'''
    orderrec = Orderrec.query.get_or_404(id)
    # if not g.current_user.can(Permission.ADMIN):
    #     return error_response(403)

    data = request.get_json()
    print('update_orderrec: ', data)
    if not data:
        return bad_request('You must post JSON data.')
    message = {}

    if message:
        return bad_request(message)

    orderrec.status_code = data.get('status_code')
    orderrec.opinion_text = data.get('opinion_text')
    orderrec.auditor_id = g.current_user.id
    more_orderrec_to_be_audit = 0
    
    for orderrec in orderrec.order.orderrecs:
        if orderrec.status_code == 0:
            more_orderrec_to_be_audit = 1

    if data.get('status_code') == 9:
        orderrec.order.status_code = 9
        orderrec.order.visit.status_code = 9
    elif data.get('status_code') == 3:
        if not more_orderrec_to_be_audit:
            orderrec.order.status_code = 3
            orderrec.order.visit.status_code = 3

    orderrec.from_dict(data)
    db.session.commit()
    return jsonify(orderrec.to_dict())


