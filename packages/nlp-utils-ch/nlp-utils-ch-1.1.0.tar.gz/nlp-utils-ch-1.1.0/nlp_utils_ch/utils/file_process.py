# -*- coding: utf-8 -*-
# Author : Jesper
# Date：   2020/6/30 21:19
# Description :
import json
import pickle
from nlp_utils_ch.utils.logger import log
from nlp_utils_ch.data_process.csv_process import read_csv_data, save_csv_data


def save_pickle(data, file_path):
	'''
	保存成pickle文件
	:param data:
	:param file_name:
	:param pickle_path:
	:return:
	'''
	with open(file_path, 'wb') as f:
		pickle.dump(data, f)


def load_pickle(input_file):
	'''
	读取pickle文件
	:param pickle_path:
	:param file_name:
	:return:
	'''
	with open(str(input_file), 'rb') as f:
		data = pickle.load(f)
	return data


def save_json(data, file_path, ensure_ascii=False, indent=4):
	'''
	保存成json文件
	:param data:
	:param json_path:
	:param file_name:
	:return:
	'''

	with open(str(file_path), 'w') as f:
		json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(file_path):
	'''
	加载json文件
	:param json_path:
	:param file_name:
	:return:
	'''
	with open(str(file_path), 'r') as f:
		data = json.load(f)
	return data


## 解决excel直接复制到csv，因换行,tab符号导致顺序错乱
def excel_to_csv(src_path, tgt_path, replace_chars=["\n", "\t"],
				 header=True,
				 content_col="content",
				 src_file_type="excel"):
	""":arg
	src_file_type: excel/csv
	"""
	# import 写在函数内，避免其它调用时
	import pandas as pd
	if src_file_type == "excel":
		raw_data = pd.read_excel(src_path, encoding="utf-8", errors='ignore')
	elif src_file_type == "csv":
		raw_data = pd.read_csv(src_path, encoding="utf-8")
	else:
		raise NotImplemented
	log.info("raw_data count:{}".format(len(raw_data)))
	col_names = raw_data.columns.values
	res_data = list()
	for i in range(len(raw_data)):
		line_list = list()
		for _col_name in col_names:
			_value = str(raw_data[_col_name][i])
			if _col_name == content_col:
				for _char in replace_chars:
					_value = _value.replace(_char, " ")
			line_list.append(_value)
		res_data.append("\t".join(line_list))

	with open(tgt_path, "w") as f:
		for _line in res_data:
			# for _char in replace_chars:
			_line = _line.replace("\n", " ")
			f.write(_line + "\n")


def csv_to_tsv(src_path, tgt_path):
	"""
	csv转为tsv，并去除tab符和换符
	"""
	import pandas as pd
	data = pd.read_csv(src_path)
	col_names = data.columns
	for _col_name in col_names:
		data[_col_name] = data[_col_name].apply(lambda x: str(x).strip().replace("'\n", " ").
												replace("'\t", " ").replace("'\r", " ").
												replace("'\n\r", " "))
	data.to_csv(tgt_path, sep="\t", index=False)


def sort_big_file_data(src_path, tgt_path, field):
	data = read_csv_data(src_path)
	data = sort_data(data, field)
	save_csv_data(data, tgt_path)


def sort_data(data, field):
	data = sorted(data, key=lambda x: x[field], reverse=True)
	return data
