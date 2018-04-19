# coding=utf-8
from . import api
from flask import session, current_app, jsonify, request

from iHome import db, constants
from iHome.models import User
from iHome.response_code import RET
from iHome.utils.image_storage import image_storage


@api.route('/user/avatar', methods=['POST'])
def set_user_avatar():
    """
    保存上传用户的头像:
    0. todo: 判断用户是否登录
    1. 获取上传头像文件
    2. 上传头像文件到七牛云系统
    3. 设置用户的头像记录
    4. 返回应答，上传头像成功
    """
    # 1. 获取上传头像文件
    file = request.files.get('avatar')

    if not file:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 2. 上传头像文件到七牛云系统
    try:
        key = image_storage(file.read())
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传头像失败')

    # 3. 设置用户的头像记录
    user_id = session.get('user_id')

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户信息失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    user.avatar_url = key

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存头像记录失败')

    # 4. 返回应答，上传头像成功
    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg='上传头像成功', data={'avatar_url': avatar_url})


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
    # resp = {
    #     'user_id': user.id,
    #     'username': user.name,
    #     'avatar_url': constants.QINIU_DOMIN_PREFIX + (user.avatar_url if user.avatar_url else '')
    # }

    return jsonify(errno=RET.OK, errmsg='OK', data=user.to_dict())
