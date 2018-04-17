# coding=utf-8
import redis
import logging


class Config(object):
    """配置类"""
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


class DevelopmentConfig(Config):
    """开发阶段的配置类"""
    DEBUG = True
    # 设置开发阶段的日志等级
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产阶段的配置类"""
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@172.16.179.139:3306/ihome'
    # 设置开发阶段的日志等级
    LOG_LEVEL = logging.WARNING


config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}