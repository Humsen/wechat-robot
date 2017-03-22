# coding: utf-8

import os
import requests
import time
from wxpy import *
import json

#图灵机器人
tuling = Tuling(api_key='0d26f7c76ecf4623a536368eaf3d26ea')

#微信自动回复
#robot = Robot()
robot=Bot(True,1)

#mps = robot.mps(update=True)
group_1 = robot.groups().search('来呀。来呀。')[0]
#group_2 = robot.groups().search('只是爱要怎么说 出口')[0]
group_3 = robot.groups().search('421永不断片')[0]

# 回复来自其他好友、群聊和公众号的消息
@robot.register([Friend])
def reply_my_friend(msg):
    tuling.do_reply(msg)

# 如果是群聊，但没有被 @，则不回复
@robot.register([Group])
def auto_reply(msg):
    if not (isinstance(msg.sender, Group) and not msg.is_at):
        tuling.do_reply(msg)

 # 如果是群聊，而且是语音，但没有被 @，则不回复
@robot.register([Group],RECORDING)
def auto_reply(msg):
    if not (isinstance(msg.sender, Group) and not msg.is_at):
        replys = '机器人暂时无法识别语音哦。'
        return replys

@robot.register([Friend],RECORDING )
def auto_reply(msg):
    replys = '机器人暂时无法识别语音哦。'
    return replys

#忽略公众号自动回复
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

#接收一些群
@robot.register([group_1,group_3])
def ignore(msg):
    tuling.do_reply(msg)

groups = robot.groups(True)
#整点报时
while 1:
    hour = time.strftime('%H', time.localtime(time.time()))
    minutes = time.strftime('%M', time.localtime(time.time()))
    second = time.strftime('%S', time.localtime(time.time()))

    if ('00' == minutes and '00' == second):
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        for group in groups:
            group.send('为您整点报时：\n{}'.format(nowTime))
        time.sleep(2)

# 自动接受添加好友请求
@robot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    if 'wxpy' in msg.text.lower():
        new_friend = robot.accept_friend(msg.card)
        # 或 new_friend = msg.card.accept()
        # 向新的好友发送消息
        new_friend.send('哈哈，我自动接受了你的好友请求')

# 开始监听和自动处理消息
#robot.start()
embed()
os.system("pause")