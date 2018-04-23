# coding=utf-8
# 此文件中定义和订单相关api
from datetime import datetime

from flask import current_app
from flask import g
from flask import request, jsonify

from iHome import db
from iHome.models import House, Order
from iHome.response_code import RET
from iHome.utils.commons import login_required
from . import api


# /orders?role=lodger
# role=lodger, 代表以房客的身份查询预订其他人房屋的订单
# role=landlord, 代表以房东的身份查询其他人预订自己房屋的订单
@api.route('/orders')
@login_required
def get_order_list():
    """
    获取用户的订单信息:
    1. 获取查询订单时用户的身份
        1.1 如果role==lodger, 代表以房客的身份查询预订其他人房屋的订单
        1.2 如果role=landlord, 代表以房东的身份查询其他人预订自己房屋的订单
    2. 组织数据，返回应答
    """ 
    # 1. 获取查询订单时用户的身份
    role = request.args.get('role')
    if role not in ('lodger', 'landlord'):
        return jsonify(errno=RET.PARAMERR, errmsg='数据错误')

    user_id = g.user_id

    try:
        if role == 'lodger':
            # 1.1 如果role==lodger, 代表以房客的身份查询预订其他人房屋的订单
            orders = Order.query.filter(Order.user_id == user_id).all()
        else:
            # 1.2 如果role=landlord, 代表以房东的身份查询其他人预订自己房屋的订单
            # 获取房东的所有房屋的信息
            houses = House.query.filter(House.user_id == user_id).all()
            houses_id_li = [house.id for house in houses]
            # 查询出订单中房屋的id在houses_id_li列表中的数据
            orders = Order.query.filter(Order.house_id.in_(houses_id_li)).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询订单信息失败')
    
    # 2. 组织数据，返回应答
    orders_dict_li = []
    for order in orders:
        orders_dict_li.append(order.to_dict())

    return jsonify(errno=RET.OK, errmsg='OK', data=orders_dict_li)


# @api.route('/orders')
# @login_required
# def get_order_list():
#     """
#     获取用户的订单信息:
#     1. 根据用户的id查询出用户的所有订单的信息，按照订单的创建时间进行排序
#     2. 组织数据，返回应答
#     """
#     # 1. 根据用户的id查询出用户的所有订单的信息，按照订单的创建时间进行排序
#     user_id = g.user_id
#     try:
#         orders = Order.query.filter(Order.user_id == user_id).all()
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg='查询订单失败')
#
#     # 2. 组织数据，返回应答
#     orders_dict_li = []
#     for order in orders:
#         orders_dict_li.append(order.to_dict())
#
#     return jsonify(errno=RET.OK, errmsg='OK', data=orders_dict_li)


@api.route('/orders', methods=['POST'])
@login_required
def save_order_info():
    """
    保存房屋预订订单的信息:
    1. 接收参数(房屋id, 起始时间，结束时间) 并进行参数校验
    2. 根据房屋id查询房屋信息（如果查不到，说明房屋信息不存在)
    3. 根据入住起始时间和结束时间查询订单是否有冲突
    4. 创建Order对象并保存订单信息
    5. 把订单信息添加进数据库
    6. 返回应答，订单创建成功
    """
    # 1. 接收参数(房屋id, 起始时间，结束时间) 并进行参数校验
    req_dict = request.json
    house_id = req_dict.get('house_id')
    start_date = req_dict.get('start_date')
    end_date = req_dict.get('end_date')
    
    if not all([house_id, start_date, end_date]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
        
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        assert start_date < end_date, Exception('起始时间大于结束时间')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 2. 根据房屋id查询房屋信息（如果查不到，说明房屋信息不存在)
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询房屋信息失败')

    if not house:
        return jsonify(errno=RET.NODATA, errmsg='房屋不存在')

    # 3. 根据入住起始时间和结束时间查询订单是否有冲突
    try:
        conflict_orders_count = Order.query.filter(end_date > Order.begin_date,
                                                start_date < Order.end_date,
                                                Order.house_id == house_id).count()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询冲突订单失败')

    if conflict_orders_count > 0:
        # 存在冲突订单
        return jsonify(errno=RET.DATAERR, errmsg='房屋已被预订')

    # 4. 创建Order对象并保存订单信息
    days = (end_date - start_date).days
    order = Order()
    order.user_id = g.user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = days
    order.house_price = house.price
    order.amount = house.price * days

    # 房屋预订量加1
    house.order_count += 1

    # 5. 把订单信息添加进数据库
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存订单信息失败')
        
    # 6. 返回应答，订单创建成功
    return jsonify(errno=RET.OK, errmsg='OK')