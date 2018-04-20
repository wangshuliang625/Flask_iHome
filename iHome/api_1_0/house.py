# coding=utf-8
# 此文件定义和房屋有关的api
from . import api

from iHome.models import Area
from iHome.response_code import RET

from flask import current_app, jsonify


@api.route('/areas')
def get_areas():
    """
    获取城区信息:
    1. 从数据库中获取所有的城区信息
    2. 组织数据，返回应答
    """
    # 1. 从数据库中获取所有的城区信息
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询城区信息失败')

    # 2. 组织数据，返回应答
    areas_dict_li = []
    for area in areas:
        areas_dict_li.append(area.to_dict())

    return jsonify(errno=RET.OK, errmsg='OK', data=areas_dict_li)