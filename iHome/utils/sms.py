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


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

def sendTemplateSMS(to, datas, tempId):
    # ��ʼ��REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.iteritems():

        if k == 'templateSMS':
            for k, s in v.iteritems():
                print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)

# sendTemplateSMS(�ֻ�����,��������,ģ��Id)

if __name__ == '__main__':
    # ���Զ��ŷ���
    sendTemplateSMS('15396961822', ['100100', '5'], 1)
