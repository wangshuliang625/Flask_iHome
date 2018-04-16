# coding=utf-8
# 提供图片验证码和短信验证码
from . import api
from iHome import redis_store, constants
from iHome.response_code import RET
from iHome.utils.captcha.captcha import captcha

from flask import request, jsonify, make_response, abort


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
        print e
        return jsonify(errno=RET.DBERR, errmsg='保存图片验证码失败')

    # 4. 返回验证码图片
    response = make_response(data)
    # 设置响应内容的类型
    response.headers['Content-Type'] = 'image/jpg'
    return response



