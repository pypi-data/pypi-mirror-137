#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2021/7/20  11:13
# @Description :

from nlp_utils_ch.utils.logger import log


def read_csv_data(file_path, col_names=None, header=True, sep="\t", ignore_null=False):
	data = list()
	with open(file_path, "r") as f:
		count = 0
		for line in f.readlines():

			if count == 0 and header is True:
				col_names = line.strip().split(sep)
				count += 1
				continue

			line_list = line.strip("\n").split(sep)
			if ignore_null is True and len(line_list) < len(col_names):
				for i in range(len(col_names) - len(line_list)):
					line_list.append("")

			tmp_dict = dict()
			try:
				for i, col_name in enumerate(col_names):
					tmp_dict[col_name] = line_list[i]
				data.append(tmp_dict)
			except Exception as e:
				log.info("Error line:{}".format(line))
				# log.error(e, exc_info=True)

	log.info("data num:{}".format(len(data)))
	log.info("data example 2:{}".format(data[:2]))
	return data


def save_csv_data(data, file_path, col_names=None, exist_header=True):
	with open(file_path, "w") as f:
		if not col_names and data:
			col_names = data[0].keys()

		if exist_header:
			f.write("\t".join(col_names) + "\n")
		for item in data:
			line_str = "\t".join([str(item[x]) for x in col_names])
			f.write(line_str + "\n")
