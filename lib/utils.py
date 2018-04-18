# -*- coding: utf-8 -*-    @Time    : 18-1-17 下午9:25
# @Author  : QiHanFang     @Email   : qihanfang@foxmail.com

import hashlib
import time
import re


def create_id():
    m = hashlib.md5(str(time.time()).encode('utf8'))
    return m.hexdigest()


def hash_pwd(pwd):
    m = hashlib.md5(pwd.encode('utf8'))
    return m.hexdigest()


def format_print(s, length):
    '''格式化输出, 区分出汉字和ascii的填充字符'''
    if re.match('[\u4e00-\u9fa5]+', s):
        return s.ljust(length, chr(12288))  # 中文
    else:
        return s.ljust(length, ' ')


if __name__ == '__main__':
    print(format_print('华盛顿阿萨德', 12), format_print('哈哈', 12))
    print(format_print('欺负谁厉害', 12), format_print('安徽省', 12))




