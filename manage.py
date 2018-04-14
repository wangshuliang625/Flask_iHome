# coding=utf-8
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    """配置类"""
    DEBUG = True

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@172.16.179.139:3306/ihome26'
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = '172.16.179.139'
    REDIS_PORT = 6379

# 创建Flask应用程序实例
app = Flask(__name__)

# 加载配置
app.config.from_object(Config)

# 创建db对象
db = SQLAlchemy(app)

# redis
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)


@app.route('/')
def index():
    # 测试redis
    # 因为这里是测试代码，所以注释掉
    # redis_store.set('name', 'laowang')
    return 'index'

if __name__ == '__main__':
    # 运行开发web服务器
    app.run()