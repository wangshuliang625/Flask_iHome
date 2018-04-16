# coding=utf-8
from . import api
from iHome import redis_store


# 使用蓝图注册路由
@api.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis
    # 因为这里是测试代码，所以注释掉
    redis_store.set('name', 'laowang')
    # 测试session
    # session['name'] = 'smart'
    return 'index'
