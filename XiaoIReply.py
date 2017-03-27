# -*- coding: utf-8 -*-

#小i机器人
from wxpy import XiaoI

xiaoI = XiaoI('oxlPCEDxod6n', 'jjZQvJmwIqjaTbuDDwe6')

def auto_reply(msg):
    xiaoI.do_reply(msg)

def text_reply(msg):
    return xiaoI.reply_text(msg)