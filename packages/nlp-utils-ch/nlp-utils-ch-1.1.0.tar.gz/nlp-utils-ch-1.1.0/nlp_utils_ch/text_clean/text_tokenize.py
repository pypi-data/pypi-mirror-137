# -*- coding: utf-8 -*-
"""
   Author :        Jesper
   Date：          2020/4/9 14:38
   Description :
   Changed by:
"""
import copy
from nlp_utils_ch.char_judgement.char_judgement import is_number, is_alphabet

def whitespace_tokenize(text, sep=" "):
	"""Runs basic whitespace cleaning and splitting on a piece of text."""
	text = text.strip()
	if not text:
		return []
	tokens = text.split(sep)
	return tokens

def split_string(text, sep=" ", keep_sep=False):
	res_text_list = list()
	for _word in text.split(sep):
		if keep_sep is False:
			if len(_word) != 0:
				res_text_list.append(_word)
		else:
			res_text_list.append(_word)
	return res_text_list

def token_en_number_seq_words(text, save_position=False):
	text = text.replace(" ", "")
	remain_text = ""
	en_num_words = list()
	i = 0
	while i < len(text):
		j = copy.deepcopy(i)
		while j < len(text) and any([is_alphabet(text[j]), is_number(text[j])]):
			j += 1

		if j != i:

			# en_num_position.append([i, j])
			if save_position:
				en_num_words.append({
								"word": text[i:j],
								"position": [i, j]
				})
			else:
				en_num_words.append(text[i:j])
			remain_text += " "
			i = copy.deepcopy(j)

		else:
			remain_text += text[i]
			i += 1
	# print(en_num_words)
	# print(remain_text)
	return en_num_words, remain_text
