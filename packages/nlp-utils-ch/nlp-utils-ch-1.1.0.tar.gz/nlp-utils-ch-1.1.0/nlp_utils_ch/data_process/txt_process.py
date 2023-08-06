#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2021/8/3  17:02
# @Description :


def read_txt_data(file_path, linefeed_keep=False):
	with open(file_path, "r") as f:
		data = f.readlines()
	if linefeed_keep is True:
		return data
	else:
		data = [x.strip() for x in data]
		return data


def save_txt_data(data, file_path, exist_linefeed=False):
	with open(file_path, "w") as f:
		for line in data:
			if exist_linefeed:
				f.write(line)
			else:
				f.write(line + "\n")

