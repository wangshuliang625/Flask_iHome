# coding=utf-8
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import config_dict


# 创建db对象
db = SQLAlchemy()

redis_store = None


# 工厂方法: 根据传入的参数不同创建不同环境下的app的对象
def create_app(config_name):
    # 创建Flask应用程序实例
    app = Flask(__name__)

    # 获取对应的配置类
    config_cls = config_dict[config_name]

    # 加载配置
    app.config.from_object(config_cls)

    # db对象关联app
    db.init_app(app)

    # redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT)

    # 开启csrf保护
    CSRFProtect(app)

    # session存储
    Session(app)

    # 注册蓝图
    from iHome.api_1_0 import api
    app.register_blueprint(api, url_prefix='/api/v1.0')
    from iHome.web_html import html
    app.register_blueprint(html)

    return app
