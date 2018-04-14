# coding=utf-8
import redis
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session


class Config(object):
    """配置类"""
    DEBUG = True

    # 设置SECRET_KEY
    SECRET_KEY = 'qyEzGidVnaRZNInFA6lO7AoPgIJGr83Em+wXttn8rBEGnbRswiviq5moyKDXG21j'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@172.16.179.139:3306/ihome26'
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = '172.16.179.139'
    REDIS_PORT = 6379

    # session存储设置
    # 设置session存储到redis中
    SESSION_TYPE = 'redis'
    # 设置存储session的redis的地址
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 设置session信息加密
    SESSION_USE_SIGNER = True
    # 设置session的过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2

# 创建Flask应用程序实例
app = Flask(__name__)

# 加载配置
app.config.from_object(Config)

# 创建db对象
db = SQLAlchemy(app)

# redis
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 开启csrf保护
CSRFProtect(app)

# session存储
Session(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis
    # 因为这里是测试代码，所以注释掉
    # redis_store.set('name', 'laowang')
    # 测试session
    # session['name'] = 'smart'
    return 'index'

if __name__ == '__main__':
    # 运行开发web服务器
    app.run()