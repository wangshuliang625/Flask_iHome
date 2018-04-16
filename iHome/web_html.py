# coding=utf-8
from flask import Blueprint, current_app

html = Blueprint('html', __name__)


@html.route('/<file_name>')
def send_html_file(file_name):
    # 获取静态页面
    file_name = 'html/' + file_name

    # 获取对应的静态页面并返回给浏览器
    return current_app.send_static_file(file_name)

