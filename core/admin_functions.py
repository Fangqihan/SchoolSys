# -*- coding: utf-8 -*-   @Time    : 18-1-18 下午4:01
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com
from core.models import *


def display_schools_info():
    """打印所有的学校对象"""
    school_lst = School.get_all_objects()
    print('分校列表'.center(20, '-'))
    if school_lst:
        print('学校名称'.ljust(12), '学校地址')
        for school in school_lst:
            print(str(school.name).ljust(12), str(school.address))
    else:
        print('请创建先学校')
    print()




