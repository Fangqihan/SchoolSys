# -*- coding: utf-8 -*-   @Time    : 18-1-17 下午12:56
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com
# 具体参考网址: https://github.com/Fangqihan/SchoolSys


import sys
import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)

from core.teacher_operations import *
from core.student_operations import *
from core.admin_operations import *


while True:
    print('学校系统主界面'.center(20, '-'))
    choice = input('1.学生界面\n2.讲师界面\n\033[1;31m3.管理员界面(隐藏属性)\033[0m\n请输入对应的编号(\033[1;35m 退出系统:q \033[0m)>>> ').strip()
    print()

    # 学生操作界面
    if choice == '1':
        while True:
            print('学生操作界面'.center(20, '-'))
            tip = input('1.报名注册\n2.缴费激活\n3.阶段考试\n4.退出登录\n(请输入对应的编号)>>> ')
            if tip == '1':
                student_enroll()
            elif tip == '2':
                students_pay_tuition()
                input()
            elif tip == '3':
                take_exam()
            elif tip == '4':
                print()
                choice = input('退出系统(q)>>> ')
                if choice == 'q' or choice == 'quit':
                    student_logout()
                    break

    # 教师操作界面
    elif choice == '2':
        while True:
            print('教师操作界面'.center(20, '-'))
            choice = input('1.查看班级信息\n2.修改学生成绩\n3.返回主界面\n请输入编号 >>> ').strip()
            print()
            if choice == '1':
                display_class_students_info()
                input()
            elif choice == '2':
                change_class_students_info()
                input()
            elif choice == '3':
                tip = input('确定返回主界面(q)>>> ')
                if tip == 'q' or tip == 'quit':
                    teacher_logout()
                    break

    # 管理员操作界面
    elif choice == '3':
        while True:
            tip = input(
'''------管理员操作界面-------
1.引进课程
2.招收讲师
3.成立班级
4.本校课程信息
5.本校班级信息
6.本校老师信息
7.本校学生信息
8.新建学校
9.返回主界面
-------------------------------
(请输入对应的操作编号)>>> ''')
            if tip == '2':
                create_teacher()
                input()
            elif tip == '3':
                create_class()
                input()
            elif tip == '1':
                create_course()
                input()
            elif tip == '4':
                display_school_courses_info()
                input()
            elif tip == '6':
                display_school_teachers_info()
                input()
            elif tip == '5':
                display_school_classes_info()
                input()
            elif tip == '7':
                display_school_students_info()
                input()
            elif tip == '8':
                # 直接进入新的学校进行管理
                open_school()
                input()
            elif tip == '9':
                choice = input('返回主界面(q) >>> ')
                if choice == 'q' or choice == 'quit':
                    admin_logout()
                    break

    elif choice == 'q':
        choice = input('\033[1;35m 退出系统?(q) \033[0m>>> ')
        if choice == 'q' or choice == 'quit':
            exit('欢迎下次再来')



