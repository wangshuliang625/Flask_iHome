# coding=utf-8
from iHome import app, db

# from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, Manager


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