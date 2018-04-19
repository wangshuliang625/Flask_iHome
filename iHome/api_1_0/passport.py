# coding=utf-8
import json
import re
from . import api
from iHome import redis_store, db
from iHome.response_code import RET
from iHome.models import User

from flask import request, jsonify, current_app, session


@api.route('/session', methods=['DELETE'])
def logout():
    """
    退出用户登录:
    1. 清除session中用户的登录信息
    2. 返回应答，退出登录成功
    """
    # 1. 清除session中用户的登录信息
    session.clear()

    # 2. 返回应答，退出登录成功
    return jsonify(errno=RET.OK, errmsg='退出登录成功')


@api.route('/session', methods=['POST'])
def login():
    """
    用户登录功能:
    1. 获取参数（手机号，密码）并参数校验
    2. 根据手机号查询用户的信息（如果查询不到，用户不存在）
    3. 校验用户的密码是否正确，如果正确
    4. 在session中记录用户的登录状态
    5. 返回应答，登录成功
    """
    # 1. 获取参数（手机号，密码）并参数校验
    req_dict = request.json
    mobile = req_dict.get('mobile')
    password = req_dict.get('password')

    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    if not re.match(r'^1[3456789]\d{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确')

    # 2. 根据手机号查询用户的信息（如果查询不到，用户不存在）
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    # 3. 校验用户的密码是否正确，如果正确
    if not user.check_user_password(password):
        return jsonify(errno=RET.PWDERR, errmsg='登录密码错误')

    # 4. 在session中记录用户的登录状态
    session['user_id'] = user.id
    session['username'] = user.name
    session['mobile'] = user.mobile

    # 5. 返回应答，登录成功
    return jsonify(errno=RET.OK, errmsg='登录成功')


@api.route('/users', methods=['POST'])
def register():
    """
    注册用户的功能:
    1. 获取参数（手机号，短信验证码，密码）和 参数校验
    2. 从redis中获取短信验证码（如果获取不到，短信验证码过期)
    3. 对比短信验证码，如果一致
    4. 创建User并保存注册用户的信息
    5. 添加用户信息到数据库
    6. 返回应答，告诉注册成功
    """
    # 1. 获取参数（手机号，短信验证码，密码）和 参数校验
    # req_data = request.data
    # req_dict = json.loads(req_data)
    # req_dict = request.get_json()
    req_dict = request.json

    mobile = req_dict.get('mobile')
    phonecode = req_dict.get('phonecode')
    password = req_dict.get('password')

    if not all([mobile, phonecode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 2. 从redis中获取短信验证码（如果获取不到，短信验证码过期)
    try:
        sms_code = redis_store.get('sms_code:%s' % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询短信验证码失败')

    if not sms_code:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码已过期')

    # 3. 对比短信验证码，如果一致
    if sms_code != phonecode:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码错误')

    # 补充: 校验手机号是否已经被注册
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        user = None
        current_app.logger.error(e)

    if user:
        # 手机号已经被注册
        return jsonify(errno=RET.DATAEXIST, errmsg='手机号已经被注册')

    # 4. 创建User并保存注册用户的信息
    user = User()
    user.mobile = mobile
    # 用户名默认使用注册手机号
    user.name = mobile
    # todo: 注册密码加密保存
    user.password = password

    # 5. 添加用户信息到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存用户信息失败')

    # 补充：在session中记录用户的登录状态
    session['user_id'] = user.id
    session['username'] = user.name
    session['mobile'] = user.mobile

    # 6. 返回应答，告诉注册成功
    return jsonify(errno=RET.OK, errmsg='注册成功')
