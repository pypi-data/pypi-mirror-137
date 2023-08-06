#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2021/9/27  16:13
# @Description :

from collections import Counter, defaultdict
from nlp_utils_ch.utils.logger import log

def suffix_most_common(words_list, suffix_len=2, exclude_count=3, show_topn_suffix=0):
    suffix_map = defaultdict(int)
    for _word in words_list:
        if len(_word) > suffix_len:
            suffix_word = _word[-suffix_len:]
            suffix_map[suffix_word] = suffix_map.get(suffix_word, 0) + 1

    suffix_map = filter(lambda x: x[1] >= exclude_count, suffix_map.items())
    suffix_map = dict(suffix_map)
    res_words = list()
    exclude_words = list()
    if show_topn_suffix > 0:
        to_show_suffix_map = sorted(suffix_map.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        # to_show_suffix_map = [ v for v in sorted(suffix_map.values())]
        log.info("topn suffix:{}".format(to_show_suffix_map[:show_topn_suffix]))


    for _word in words_list:
        if len(_word) >= suffix_len:
            _suffix_word = _word[-suffix_len:]
            if _suffix_word not in suffix_map:
                res_words.append(_word)
            else:
                exclude_words.append(_word)

        else:
            res_words.append(_word)

    return res_words




if __name__ == '__main__':
    words = ["可爱见", "哈爱见", "爱见", "没左左"]
    res = suffix_most_common(words)
    # print(res)
