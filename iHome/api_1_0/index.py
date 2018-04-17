# coding=utf-8
import logging
from . import api
from iHome import redis_store

from flask import current_app


# 使用蓝图注册路由
@api.route('/test', methods=['GET', 'POST'])
def index():
    # 测试redis
    # 因为这里是测试代码，所以注释掉
    # redis_store.set('name', 'laowang')
    # 测试session
    # session['name'] = 'smart'

    # logging.fatal('Fatal Message')
    # logging.error('Error Message')
    # logging.warning('Warning Message')
    # logging.info('Info Message')
    # logging.debug('Debug Message')

    current_app.logger.fatal('Fatal Message')
    current_app.logger.error('Error Message')
    current_app.logger.warning('Warning Message')
    current_app.logger.info('Info Message')
    current_app.logger.debug('Debug Message')
    # 测试日志输出
    return 'index'
