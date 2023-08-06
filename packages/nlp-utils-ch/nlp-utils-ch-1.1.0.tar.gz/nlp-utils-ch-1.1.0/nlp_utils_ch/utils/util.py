#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2021/9/7  11:18
# @Description :


def remove_duplicate_keep_order(lines):
	res_line = list()
	res_set = set()
	for line in lines:
		if line not in res_set:
			res_line.append(line)
			res_set.add(line)
	return res_line


def unique_query(raw_list):
	res_list = list()
	for item in raw_list:
		if item not in res_list:
			res_list.append(item)
	return res_list
