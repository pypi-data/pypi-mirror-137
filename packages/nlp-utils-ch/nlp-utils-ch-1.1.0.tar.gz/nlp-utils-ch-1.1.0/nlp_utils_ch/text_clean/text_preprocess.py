#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2020/12/22 10:11
# @Description :
import re

def filter_redundant_char(text):
    text = text.lower()
    # 去除网址
    text = re.sub(r"(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b", "", text)
    # 合并正文中过多的空格
    text = re.sub(r"\s+", " ", text)
    # 去除网页符号
    html_re = re.compile(r'<[^>]+>', re.S)
    text = html_re.sub('', text)

    uid_re = re.compile(r'^\d{n}', re.S)
    # text = uid_re.sub('', text)
    text = re.sub('uid[:：][0-9]+', '', text)
    return text


if __name__ == '__main__':
    text = "{'describe':'画渣一个','imgs':['https://upload-bbs.mihoyo.com/upload/2020/07/08/100898502/fa2b5ff511541be3270d9df2f6ca65fa_2660021923020391956.jpg','https://upload-bbs.mihoyo.com/upload/2020/07/08/100898502/bac9952afd28723ae68ec368a9739d86_2899968460626170607.jpg']}"
    res = filter_redundant_char(text)
    print(res)
