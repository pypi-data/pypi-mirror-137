#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2021/7/20  10:38
# @Description :

from nlp_utils_ch.utils.logger import log


def read_table_data(file_path, col_names=None, header=False, sep="\t"):
	data = list()
	with open(file_path, "r") as f:
		count = 0
		for line in f.readlines():

			if count == 0 and header is True:
				col_names = line.strip().split(sep)
				count += 1
				continue

			line_list = line.strip().split(sep)
			assert len(col_names) == len(line_list)
			tmp_dict = dict()
			for i, col_name in enumerate(col_names):
				tmp_dict[col_name] = line_list[i]
			data.append(tmp_dict)
	log.info("data num:{}".format(len(data)))
	log.info("data example 2:{}".format(data[:2]))
	return data

