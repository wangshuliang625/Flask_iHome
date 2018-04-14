# coding=utf-8
import redis
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session

from config import DevelopmentConfig

# 创建Flask应用程序实例
app = Flask(__name__)

# 加载配置
app.config.from_object(DevelopmentConfig)

# 创建db对象
db = SQLAlchemy(app)

# redis
redis_store = redis.StrictRedis(host=DevelopmentConfig.REDIS_HOST, port=DevelopmentConfig.REDIS_PORT)

# 开启csrf保护
CSRFProtect(app)

# session存储
Session(app)