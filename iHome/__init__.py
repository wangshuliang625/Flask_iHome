# coding=utf-8
import redis
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session

from config import config_dict

# 创建db对象
db = SQLAlchemy()


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
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT)

    # 开启csrf保护
    CSRFProtect(app)

    # session存储
    Session(app)

    return app
