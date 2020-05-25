#!/usr/bin/env python
#coding=utf-8
def split_text(text, length):
    text_list=[]
    tmp = text[:int(length)]
    # print(tmp)
    # 将固定长度的字符串添加到列表中
    text_list.append(tmp)
    # 将原串替换
    text = text.replace(tmp, '')
    if len(text) < length + 1:
        # 直接添加或者舍弃
        text_list.append(text)
    else:
        split_text(text, length)
    return text_list