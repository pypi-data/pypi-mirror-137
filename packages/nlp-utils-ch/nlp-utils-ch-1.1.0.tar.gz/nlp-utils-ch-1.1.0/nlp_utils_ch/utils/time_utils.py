#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2021/10/21  17:48
# @Description :
import time

def print_run_time(func):
	def wrapper(*args, **kw):
		local_time = time.time()
		func(*args, **kw)
		print('current Function [%s] run time is %.2fs' % (func.__name__ ,time.time() - local_time))
	return wrapper
