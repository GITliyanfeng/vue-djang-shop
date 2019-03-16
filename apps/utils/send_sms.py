import requests
import json


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "xxxxxxxxxx{code}".format(code),
        }
        response = requests.post(url=self.single_send_url, data=parmas)
        res_dic = json.loads(response.text)
        return res_dic

    def send_test(self, code, mobile):
        res_dic = {
            'code': 0,
            'mobile': mobile,
            'sms': code,
            'msg': '错误',
        }
        return res_dic
