# coding=utf-8
from . import api
from flask import session, current_app, jsonify

from iHome.models import User
from iHome.response_code import RET


@api.route('/user')
def get_user_info():
    """
    获取用户的个人信息：
    0. todo: 判断用户是否登录
    1. 获取当前登录用户的id
    2. 根据id获取用户的信息（如果查不到，说明用户不存在）
    3. 组织数据，返回应答
    """
    # 1. 获取当前登录用户的id
    user_id = session.get('user_id')

    # 2. 根据id获取用户的信息（如果查不到，说明用户不存在)
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    # 3. 组织数据，返回应答
    resp = {
        'user_id': user.id,
        'username': user.name,
        'avatar_url': user.avatar_url
    }
    return jsonify(errno=RET.OK, errmsg='OK', data=resp)
