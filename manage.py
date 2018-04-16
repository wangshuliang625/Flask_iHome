# coding=utf-8
from iHome import create_app, db, models

# from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, Manager

# 需求: 在这里传入不同的信息创建出不同配置环境的app
app = create_app('development')

# 创建Manager对象
manager = Manager(app)
Migrate(app, db)
# 添加数据库迁移命令
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    # 运行开发web服务器
    # app.run()
    print app.url_map
    manager.run()
