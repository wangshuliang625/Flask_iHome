# coding=utf-8

from flask import Blueprint

# 创建蓝图对象
api = Blueprint('api_1_0', __name__)

from index import index
from verify import get_image_code
