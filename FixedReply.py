# -*- coding: utf-8 -*-

import time

import XiaoIReply
import adminData

#管理员手册
handbook_admin = '''
机器人主人：
01.私聊 启动/关闭机器人---------
    发送：启动/休眠
02.群聊 启动/关闭机器人---------
    发送：@机器人 启动/休眠
03.移出群成员---------
    发送：@机器人 移出 @被移除成员
04.私聊 添加/取消管理员---------
    发送：添加管理员 @某朋友
05.群聊 添加/取消管理员---------
    发送：@机器人 添加管理员 @某成员

其他管理员：
06.私聊 关闭机器人一分钟---------
    发送：休眠
07.群聊 关闭机器人一分钟---------
    发送：@机器人 休眠

所有管理员：
08.当前群回复/免打扰---------
    发送：@机器人 免打扰/取消免打扰
09.私聊 查看管理员列表---------
    发送：管理员列表
10.群聊 查看管理员列表--------- 
    发送：@机器人 管理员列表
11.私聊 查看管理员手册---------
    发送：管理员手册
12.群聊 查看管理员手册---------
    发送：@机器人 管理员手册
13.退出登录---------
    发送：登出'''
# print(handbook_admin)

#用户手册 娱乐
handbook_user_entertainment = '''01.笑话大全------讲个笑话
02.故事大全------讲个故事
03..歇后语-------说个歇后语
04.绕口令--------说个绕口令
05.顺口溜--------说个顺口溜
06.脑经急转弯----说个脑经急转弯
07.天气查询------南京天气
08.新闻资讯------今日新闻
09.星座运势------天秤座运势
10.吉凶查询------某个名字好不好
11.生活百科------图灵机器人简介
12.图片搜索------图灵机器人的图片
13.成龙接龙------成语接龙一诺千金
14.数字计算------3乘3等于多少
15.日期查询------今天农历多少
16.问答百科------天为什么蓝的
17.中英互译------苹果的单词是什么
18.影视搜索------最近热门电影'''

#用户手册 实践
handbook_user_practical = '''
01.快递查询---查询快递123456789
02.城市邮编---南京邮编
03.菜谱查询---回锅肉怎么做
04.果蔬报价---南京菠萝的价格
05.股票查询---腾讯股票
06.航班查询---今天南京到上海的飞机
07.列车查询---今天重庆到南京的火车
08.附近餐厅---南京江宁附近的餐厅
09.附近酒店---南京江宁附近的餐厅
10.实时路况---南京双龙大道堵车吗
11.公交查询---南京南站到新街口的公交
12.路程报价---从南京禄口机场到南京南站多少钱
13.租房信息---在南京新街口附近租房
14.汽油报价---重庆汽油的价格'''

#准点报时
def repot_time(group_free):
    while 1:
        hour = time.strftime('%H', time.localtime(time.time()))
        minutes = time.strftime('%M', time.localtime(time.time()))
        seconds = time.strftime('%S', time.localtime(time.time()))

        if (hour == '07' and minutes == '30' and seconds == '00'):
            nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            group_free[0].send(
                '早上好！\n起床啦，为您整点报时：\n{}\n------------今日天气------------\n{}'.format(nowTime, XiaoIReply.text_reply('重庆沙坪坝区天气')))
            group_free[1].send(
                '早上好！\n起床啦，为您整点报时：\n{}\n------------今日天气------------\n{}'.format(nowTime, XiaoIReply.text_reply('南京江宁区天气')))
        elif (hour == '13' and minutes == '30' and seconds == '00'):
            nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            for group in group_free:
                group.send('下午好！\n该干活了，为您整点报时：\n{}\n------------轻松一下------------\n{}'.format(nowTime, XiaoIReply.text_reply('讲个笑话')))
        elif (hour == '00' and minutes == '00' and seconds == '00'):
            nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            for group in group_free:
                group.send('晚上好！\nIt\'s 宵夜time，为您整点报时：\n{}\n----------晚安全世界----------'.format(nowTime))

        time.sleep(1)

#增加管理员函数
def admin_add(robot_master,group_admin,name,name_temp):
    if name in group_admin:
        robot_master.send('当前管理员组--{}'.format(group_admin))
        return '[{}]已经是管理员，无需再次添加！'.format(name_temp)
    else:
        group_admin.append(name)
        robot_master.send('当前管理员组--{}'.format(group_admin))
        adminData.admin_write(group_admin)
        return '已添加[{}]为管理员'.format(name_temp)

#取消管理员函数
def admin_sub(robot_master,group_admin,name, name_temp):
    for admin in group_admin:
        if (admin == name):
            group_admin.pop(group_admin.index(admin))
            robot_master.send('当前管理员组--{}'.format(group_admin))
            adminData.admin_write(group_admin)
            return '已取消[{}]的管理员身份'.format(name_temp)

# 验证入群口令
def valid(msg):
    return 'wechat' in msg.text.lower()

# 新人欢迎消息
welcome_text = '''******\U0001F389\U0001F389\U0001F389\U0001F389******\n
 欢迎 @{} 加入本群！\n\n*******************************'''
