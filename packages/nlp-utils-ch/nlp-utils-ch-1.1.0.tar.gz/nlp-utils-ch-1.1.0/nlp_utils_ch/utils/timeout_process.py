#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2020/11/30 11:09
# @Description :


import requests
import eventlet
import time

eventlet.monkey_patch()

time_limit = 3  # set timeout time 3s

with eventlet.Timeout(time_limit, False):
	while(True):
		time.sleep(1)
		print("time")
	# r = requests.get("https://me.csdn.net/dcrmg", verify=False)
	print('error')
print('over')
