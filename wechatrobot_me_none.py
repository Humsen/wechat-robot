# coding: utf-8

import os
import threading

import re
import requests
import time
from wxpy import *
import json

#微信机器人
robot=Bot()

#图灵机器人
tuling = Tuling(api_key='0d26f7c76ecf4623a536368eaf3d26ea')

#图灵机器人手动消息
def talks_robot(info = 'Husen'):
    api_url = 'http://www.tuling123.com/openapi/api'
    apikey = '0d26f7c76ecf4623a536368eaf3d26ea'
    data = {'key': apikey,'info': info}
    req = requests.post(api_url, data=data).text
    replys = json.loads(req)['text']
    return replys

admin_remark_name = "Husen"
admin_signature = '潜心修行，不卑不亢。'
# 定义远程管理员 (用于远程管理)，使用备注名更安全
remote_admin = ensure_one(robot.friends().search(remark_name=admin_remark_name,signature=admin_signature))

#mps = robot.mps(update=True)
group_1 = robot.groups().search('来呀。来呀。')[0]
#group_2 = robot.groups().search('只是爱要怎么说 出口')[0]
group_3 = robot.groups().search('421永不断片')[0]

#动态关闭除启动函数之外的注册函数
def remote_down():
    robot.registered.disable()
    robot.registered.enable(remote_up)
    robot.registered.enable(remote_admin_up)

#开启所有注册函数
def remote_reup():
    robot.registered.enable()

# 远程启动函数
@robot.register()
def remote_up(msg):
    if (msg.is_at and msg.member == remote_admin and '启动' in msg.text):
    #if ('启动' in msg.text):
         thread = threading.Thread(target=remote_reup)
         thread.start()
         thread.join()
         return '已启动'
    else:
         return

#远程管理员启动
@robot.register(remote_admin)
def remote_admin_up(msg):
    if ('启动' in msg.text):
        thread = threading.Thread(target=remote_reup)
        thread.start()
        thread.join()
        return '已启动'

# 回复来自其他好友的消息
@robot.register([Friend])
def reply_my_friend(msg):
    if (msg.is_at and msg.member == remote_admin and '休眠' in msg.text):
        thread = threading.Thread(target=remote_down)
        thread.start()
        thread.join()
        return '已休眠'
    else:
        tuling.do_reply(msg)

# 如果是群聊，但没有被 @，则不回复
@robot.register([Group],TEXT)
def auto_reply(msg):
    if(msg.is_at):
        if ('休眠' in msg.text  and msg.member == remote_admin ):
            thread = threading.Thread(target=remote_down)
            thread.start()
            thread.join()
            return '已休眠'
        elif(msg.chat.is_owner and '移出' in msg.text  and msg.member == remote_admin ):
            try:
                name_to_kick = re.search(r'移出\s*@(.+?)(?:\u2005?\s*$)', msg.text).group(1)
            except AttributeError:
                remote_admin.send('无法解析命令')
                return

            member_to_kick = ensure_one(msg.chat.search(name_to_kick))
            if member_to_kick == remote_admin:
                remote_admin.send('在尝试移出自己吗？')
                return
            else:
                member_to_kick.remove()
                return '已移出 [{}]'.format(name_to_kick)
        else:
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

#接收一些群
@robot.register([group_1,group_3])
def recieve_some(msg):
    #if ('休眠' in msg.text):
    if (msg.is_at and '休眠' in msg.text and msg.member == remote_admin ):
        thread = threading.Thread(target=remote_down)
        thread.start()
        thread.join()
        return '已休眠'
    elif (msg.is_at and msg.chat.is_owner and '移出' in msg.text and msg.member == remote_admin):
        try:
            name_to_kick = re.search(r'移出\s*@(.+?)(?:\u2005?\s*$)', msg.text).group(1)
        except AttributeError:
            remote_admin.send('无法解析命令')
            return

        member_to_kick = ensure_one(msg.chat.search(name_to_kick))
        if member_to_kick == remote_admin:
            remote_admin.send('在尝试移出自己吗？')
            return
        else:
            member_to_kick.remove()
            return '已移出 [{}]'.format(name_to_kick)
    else:
        tuling.do_reply(msg)

# 验证入群口令
def valid(msg):
    return 'wechat' in msg.text.lower()

# 邀请入群
def invite(user):
    if user in group_3:
        user.send('你已加入 {}'.format(group_3.nick_name))
    else:
        if(len(group_3) < 5):
            group_3.add_members(user, use_invitation=True)
        else:
            group_3.add_members(user, use_invitation=False)

# 响应好友消息
@robot.register([Friend], msg_types=TEXT)
def exist_friends(msg):
    if valid(msg):
        invite(msg.sender)
    else:
        tuling.do_reply(msg)

welcome_text = '''******\U0001F389\U0001F389\U0001F389\U0001F389******\n
 欢迎 @{} 加入本群！\n\n*******************************'''
# 新人欢迎消息
@robot.register([Group], NOTE)
def welcome(msg):
    try:
        new_member_name = re.search(r'邀请"(.+?)"|"(.+?)"通过', msg.text).group(1)
    except AttributeError:
        return

    return welcome_text.format(new_member_name)

#接收管理员命令
@robot.register(remote_admin)
def remote_admin_command(msg):
    if('休眠' in msg.text):
        thread = threading.Thread(target=remote_down)
        thread.start()
        thread.join()
        return '已休眠'
    elif("登出" in msg.text):
        print('已成功退出')
        robot.logout()
    else:
        tuling.do_reply(msg)

#自动接受好友请求
@robot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    new_friend = robot.accept_friend(msg.card)
    # 或 new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('哈哈，我自动接受了你的好友请求。')

    if valid(msg):
        invite(new_friend)
    else:
        return

groups = robot.groups(True)
#整点报时
while 1:
    hour = time.strftime('%H', time.localtime(time.time()))
    minutes = time.strftime('%M', time.localtime(time.time()))
    seconds = time.strftime('%S', time.localtime(time.time()))

    if (hour == '07' and minutes == '30' and seconds == '00'):
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        group_1.send('早上好！\n起床啦，为您整点报时：\n{}\n--------今日天气--------\n{}'.format(nowTime,talks_robot(info='重庆沙坪坝区天气')))
        group_3.send('早上好！\n起床啦，为您整点报时：\n{}\n--------今日天气--------\n{}'.format(nowTime,talks_robot(info='南京江宁区天气')))
    elif(hour == '13' and minutes == '30' and seconds == '00'):
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        for group in groups:
            group.send('下午好！\n该干活了，为您整点报时：\n{}\n--------轻松一下--------\n{}'.format(nowTime,talks_robot(info='讲个笑话')))
    elif (hour == '00' and minutes == '00' and seconds == '00'):
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        for group in groups:
            group.send('晚上好！\nIt\'s 宵夜time，为您整点报时：\n{}\n--------晚安全世界--------'.format(nowTime))

    time.sleep(1)

# 开始监听和自动处理消息
#robot.start()
embed()
os.system("pause")