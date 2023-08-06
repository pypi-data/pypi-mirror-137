#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2020/11/18 16:19
# @Description :

import datetime

def get_cur_date():
	now = datetime.datetime.now()
	cur_date = now.strftime("%Y-%m-%d")
	return cur_date

def get_last_nday_date(n=3):
	now = datetime.datetime.now()
	start_datetime = now - datetime.timedelta(days=n)
	start_date = start_datetime.strftime("%Y-%m-%d")
	return start_date

