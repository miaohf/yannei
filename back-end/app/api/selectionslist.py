from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Permission, Province, Customer, Visittype
from app.utils.decorator import permission_required





@bp.route('/selections/provinces', methods=['GET'])
@token_auth.login_required
def get_provinces_available():
    '''返回所有省份列表'''
    provinces = Province.query.all()
    data = {'items': [{'id': p.id, 'name': p.name} for p in provinces]}
    return jsonify(data)


@bp.route('/selections/cities/<int:province_id>/', methods=['GET'])
@token_auth.login_required
def get_cities_by_province(province_id):
    '''返回某一个省份的所有城市列表'''
    province = Province.query.get_or_404(province_id)
    data = {'items': [{'id': c.id, 'name': c.name} for c in province.cities]}
    return jsonify(data)



@bp.route('/selections/customers', methods=['GET'])
@token_auth.login_required
def get_customers_available():
    '''返回所有客户列表'''
    customers = Customer.query.all()
    data = {'items': [{'id': c.id, 'name': c.name} for c in customers]}
    return jsonify(data)


@bp.route('/selections/contactors/<int:customer_id>/', methods=['GET'])
@token_auth.login_required
def get_contactors_by_customer(customer_id):
    '''返回某一个客户的所有联系人列表'''
    customer = Customer.query.get_or_404(customer_id)
    data = {'items': [{'id': c.id, 'name': c.name + ': ' + c.mobile } for c in customer.contactors]}
    return jsonify(data)

@bp.route('/selections/addresses/<int:customer_id>/', methods=['GET'])
@token_auth.login_required
def get_addresses_by_customer(customer_id):
    '''返回某一个客户的所有联系人列表'''
    customer = Customer.query.get_or_404(customer_id)
    data = {'items': [{'id': a.id, 'name': a.address_info } for a in customer.addresses]}
    return jsonify(data)


@bp.route('/selections/visittypes', methods=['GET'])
@token_auth.login_required
def get_visittypes_available():
    '''返回所有拜访类型列表'''
    visittypes = Visittype.query.all()
    data = {'items': [{'id': vt.id, 'name': vt.name} for vt in visittypes]}
    return jsonify(data)