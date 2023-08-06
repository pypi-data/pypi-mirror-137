#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2021/7/20  10:36
# @Description :
import hashlib

def get_md5(text, num=10):
	md5 = hashlib.md5()
	md5.update(text.encode('utf-8'))
	# print(md5.hexdigest())
	return md5.hexdigest()[:num]
