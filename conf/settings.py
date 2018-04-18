# -*- coding: utf-8 -*-    @Time    : 18-1-17 下午12:56
# @Author  : QiHanFang     @Email   : qihanfang@foxmail.com

import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

HOT_COURSES = ['python', 'linux', 'go', 'java', 'php', 'c', 'c++']  # 小写
MAIN_CITIES = ['北京', '上海', '深圳', '杭州', '武汉', '广州', '长沙', '重庆', '天津', '合肥', '成都']

SCHOOL_PATH = '%s/db/schools' % BASE_DIR
CLASS_PATH = '%s/db/classes' % BASE_DIR
TEACHER_PATH = '%s/db/teachers' % BASE_DIR
STUDENT_PATH = '%s/db/students' % BASE_DIR
COURSE_PATH = '%s/db/courses' % BASE_DIR

if not os.path.exists(SCHOOL_PATH):
    os.makedirs(SCHOOL_PATH)
if not os.path.exists(CLASS_PATH):
    os.makedirs(CLASS_PATH)
if not os.path.exists(TEACHER_PATH):
    os.makedirs(TEACHER_PATH)
if not os.path.exists(STUDENT_PATH):
    os.makedirs(STUDENT_PATH)
if not os.path.exists(COURSE_PATH):
    os.makedirs(COURSE_PATH)

ADMIN_ACCOUNT = {'username': '', 'password': ''}

DEBUG = False


LOG_LEVEL = logging.INFO
LOG_PATH = "%s/log/" % BASE_DIR
LOG_TYPES = {
    'teacher': 'teacher_related.log',
    'student': 'students_related.log',
    'admin': 'admin_related.log',
}






