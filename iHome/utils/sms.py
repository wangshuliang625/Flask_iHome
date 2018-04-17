# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from iHome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8aaf070861f56d5c0161f5874194001e'

# 主帐号Token
accountToken = '8474fd8f17a647288b0d074996a7de8c'

# 应用Id
appId = '8aaf070861f56d5c0161f58741fc0025'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 单例模式
class CCP(object):
    def __new__(cls, *args, **kwargs):
        # 判断当前类有没有属性_instance, 此属性用来保存这个类的唯一对象
        if not hasattr(cls, '_instance'):
            # 创建实例对象
            obj = super(CCP, cls).__new__(cls, *args, **kwargs)
            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)

            cls._instance = obj
        # 返回单例对象
        return cls._instance

    # def __init__(self):
    #     # 初始化REST SDK
    #     self.rest = REST(serverIP, serverPort, softVersion)
    #     self.rest.setAccount(accountSid, accountToken)
    #     self.rest.setAppId(appId)

    def send_template_sms(self, to, datas, temp_id):
        # 发送模板短信
        # @param to 手机号码
        # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
        # @param $tempId 模板Id
        result = self.rest.sendTemplateSMS(to, datas, temp_id)

        if result.get('statusCode') == '000000':
            # 发送成功
            return 1
        else:
            # 发送失败
            return 0

# sendTemplateSMS(手机号码,内容数据,模板Id)

if __name__ == '__main__':
    # 测试短信发送
    # sendTemplateSMS('15396961822', ['100100', '5'], 1)
    # CCP().send_template_sms('15396961822', ['100100', '5'], 1)
    CCP().send_template_sms('15396961822', ['100100', '5'], 1)

    # 测试单例
    # obj1 = CCP()
    # obj2 = CCP()
    #
    # print id(obj1)
    # print id(obj2)
