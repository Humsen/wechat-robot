# -*- coding: utf-8 -*-

import os

from wxpy import *

#robot = Bot(True)

#robot_master = ensure_one(robot.friends().search(remark_name='Husen'))
#group_admin = [robot_master]
#print(group_admin)

#写入管理员的名称数据
def admin_write(group_admin):
    file=open('admin_data.txt','w')

    try:
        for admin in group_admin:
            file.write(str(admin) + '\n')
        file.close()
    finally:
        file.close()

#读取管理的名称数据
def admin_read(robot):
    result = []
    if not os.path.exists('admin_data.txt'):
        file = open("admin_data.txt","w")
        file.close()
    file = open("admin_data.txt", "r")

    try:
        for line in file.readlines():
            line.encode('utf-8')
            str1 = line.split(':', 1)
            str2 = str1[1].split('>', 1)
            try:
                next_admin = ensure_one(robot.friends().search(str2[0]))
            except:
                continue
            result.append(next_admin)
        file.close()
    finally:
        file.close()

    return result

#admin_read(robot)
