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
    if re.match('[\u4e00-\u9fa5]+', s):
        return s.ljust(length, chr(12288))  # 中文
    else:
        return s.ljust(length, ' ')

