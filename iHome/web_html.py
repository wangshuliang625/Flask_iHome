# coding=utf-8
from flask import Blueprint, current_app

html = Blueprint('html', __name__)


@html.route('/<re(".*"):file_name>')
def send_html_file(file_name):
    # 获取静态页面
    # 判断用户访问的是否为根路径，如果是，返回首页
    if file_name == '':
        file_name = 'index.html'

    # 判断是否访问的是网站图标，如果不是，拼接路径
    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name

    # 获取对应的静态页面并返回给浏览器
    # send_static_file('html/index.html')
    # send_static_file('html/login.html')
    return current_app.send_static_file(file_name)
