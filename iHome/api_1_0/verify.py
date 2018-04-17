# coding=utf-8
# 提供图片验证码和短信验证码
import json
import re
from . import api
from iHome import redis_store, constants
from iHome.response_code import RET
from iHome.utils.captcha.captcha import captcha

from flask import request, jsonify, make_response, abort, current_app


@api.route('/sms_code', methods=['POST'])
def send_sms_code():
    """
    发送短信验证码:
    1. 获取参数（手机号，图片验证码，图片验证码id）
    2. 判断参数的完整性并且进行参数校验
    3. 从redis中获取对应的图片验证码（如果获取不到，图片验证码过期）
    4. 对比图片验证码，如果一致
    5. 发送短信验证码
    6. 返回信息，发送短信验证码成功
    """

    # 1. 获取参数（手机号，图片验证码，图片验证码id）
    # 获取json
    req_data = request.data
    req_dict = json.loads(req_data)

    mobile = req_dict.get('mobile')
    image_code = req_dict.get('image_code')
    image_code_id = req_dict.get('image_code_id')

    # 2. 判断参数的完整性并且进行参数校验
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 校验手机号
    if not re.match(r"1[3456789]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确')

    # 3. 从redis中获取对应的图片验证码（如果获取不到，图片验证码过期）
    try:
        real_image_code = redis_store.get('imagecode:%s' % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询图片验证码错误')

    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg='图片验证码已过期')

    # 4. 对比图片验证码，如果一致
    if real_image_code != image_code:
        return jsonify(errno=RET.DATAERR, errmsg='图片验证码错误')

    # 5. todo: 发送短信验证码

    # 6. 返回信息，发送短信验证码成功
    return jsonify(errno=RET.OK, errmsg='发送短信成功')


@api.route('/image_code')
def get_image_code():
    """
    生成图片验证码：
    # 1. 获取uuid(验证码编号)
    # 2. 生成图片验证码
    # 3. 在redis中存储图片验证码
    # 4. 返回验证码图片
    """
    # 1. 获取uuid(验证码编号)
    cur_id = request.args.get('cur_id')

    if not cur_id:
        abort(403)

    # 2. 生成图片验证码
    # 图片名称  验证码文本  验证码图片的内容
    name, text, data = captcha.generate_captcha()

    # 3. 在redis中存储图片验证码
    # redis_store.set('键名', '验证码文本', '验证有效时间')
    try:
        redis_store.set('imagecode:%s' % cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存图片验证码失败')

    # 4. 返回验证码图片
    response = make_response(data)
    # 设置响应内容的类型
    response.headers['Content-Type'] = 'image/jpg'
    return response



