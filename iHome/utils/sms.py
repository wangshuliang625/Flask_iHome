# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from iHome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# ���ʺ�
accountSid = '8aaf070861f56d5c0161f5874194001e'

# ���ʺ�Token
accountToken = '8474fd8f17a647288b0d074996a7de8c'

# Ӧ��Id
appId = '8aaf070861f56d5c0161f58741fc0025'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'


# ����ģʽ
class CCP(object):
    def __new__(cls, *args, **kwargs):
        # �жϵ�ǰ����û������_instance, ��������������������Ψһ����
        if not hasattr(cls, '_instance'):
            # ����ʵ������
            obj = super(CCP, cls).__new__(cls, *args, **kwargs)
            # ��ʼ��REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)

            cls._instance = obj
        # ���ص�������
        return cls._instance

    # def __init__(self):
    #     # ��ʼ��REST SDK
    #     self.rest = REST(serverIP, serverPort, softVersion)
    #     self.rest.setAccount(accountSid, accountToken)
    #     self.rest.setAppId(appId)

    def send_template_sms(self, to, datas, temp_id):
        # ����ģ�����
        # @param to �ֻ�����
        # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
        # @param $tempId ģ��Id
        result = self.rest.sendTemplateSMS(to, datas, temp_id)

        if result.get('statusCode') == '000000':
            # ���ͳɹ�
            return 1
        else:
            # ����ʧ��
            return 0

# sendTemplateSMS(�ֻ�����,��������,ģ��Id)

if __name__ == '__main__':
    # ���Զ��ŷ���
    # sendTemplateSMS('15396961822', ['100100', '5'], 1)
    # CCP().send_template_sms('15396961822', ['100100', '5'], 1)
    CCP().send_template_sms('15396961822', ['100100', '5'], 1)

    # ���Ե���
    # obj1 = CCP()
    # obj2 = CCP()
    #
    # print id(obj1)
    # print id(obj2)
