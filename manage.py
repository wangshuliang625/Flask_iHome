# coding=utf-8
import redis
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session

from config import Config

# from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, Manager


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

# 创建Manager对象
manager = Manager(app)
Migrate(app, db)
# 添加数据库迁移命令
manager.add_command('db', MigrateCommand)


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
    # app.run()
    manager.run()