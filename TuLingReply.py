# -*- coding: utf-8 -*-

#图灵机器人
import json

import requests
from wxpy import *

tuling = Tuling(api_key='0d26f7c76ecf4623a536368eaf3d26ea')

#图灵自动消息
def auto_reply(msg):
    tuling.do_reply(msg)

#图灵机器人返回文本
def text_reply(msg):
    api_url = 'http://www.tuling123.com/openapi/api'
    apikey = '0d26f7c76ecf4623a536368eaf3d26ea'
    data = {'key': apikey,'info': msg}
    req = requests.post(api_url, data=data).text
    replys = json.loads(req)['text']
    return replys