# coding=utf-8
# 提供图片验证码和短信验证码
from . import api
from iHome.utils.captcha.captcha import captcha


@api.route('/image_code')
def get_image_code():
    """
    生成图片验证码：
    :return:
    """

    # 生成图片验证码
    # 图片名称  验证码文本  验证码图片的内容
    name, text, data = captcha.generate_captcha()

    # 返回验证码的图片
    return data



