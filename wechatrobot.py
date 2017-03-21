import os
import requests
from wxpy import *
import json

#图灵机器人
def talks_robot(info = 'Husen'):
    api_url = 'http://www.tuling123.com/openapi/api'
    apikey = '4cb9814aa00b41d38a1c0abc5a00c929'
    data = {'key': apikey,
                'info': info}
    req = requests.post(api_url, data=data).text
    replys = json.loads(req)['text']
    return replys

#微信自动回复
#robot = Robot()
robot=Bot()

# 回复来自其他好友、群聊和公众号的消息
@robot.register([Friend])
def reply_my_friend(msg):
    message = '{}'.format(msg.text)
    replys = talks_robot(info=message)+'\n\t\t\t\t\t\t\t--微信机器人自动回复'
    return replys

@robot.register([Group])
def auto_reply(msg):
    # 如果是群聊，但没有被 @，则不回复
    if not (isinstance(msg.sender, Group) and not msg.is_at):
        # 回复消息内容和类型
        message = '{}'.format(msg.text)
        replys = talks_robot(info=message)+'\n\t\t\t\t\t--微信机器人自动回复'
        return replys

@robot.register([Group],RECORDING)
def auto_reply(msg):
     # 如果是群聊，但没有被 @，则不回复
    if not (isinstance(msg.sender, Group) and not msg.is_at):
        # 回复消息内容和类型
        replys = '机器人暂时无法识别语音哦。' + '\n\t\t\t\t\t--微信机器人自动语音回复'
        return replys

@robot.register([Friend],RECORDING )
def auto_reply(msg):
     # 回复消息内容和类型
    replys = '机器人暂时无法识别语音哦。' + '\n\t\t\t\t\t--微信机器人自动语音回复'
    return replys

#忽略公众号
@robot.register([MP])
def ignore_mps(msg):
    # 啥也不做
    return

"""
#忽略一些群
@robot.register(boring_group)
def ignore(msg):
    # 啥也不做
    return
"""

# 开始监听和自动处理消息
#robot.start()
embed()

os.system("pause")
