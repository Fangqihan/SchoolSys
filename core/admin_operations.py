# -*- coding: utf-8 -*-   @Time    : 18-1-20 上午8:30
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com

from core.auth import *
from core.admin_functions import *


@admin_login_and_choose_school
def create_teacher(**kwargs):
    """在当前学校创建教师"""
    school = kwargs.get('school')
    Teacher(school)


@admin_login_and_choose_school
def create_class(**kwargs):
    """在当前学校创建班级"""
    school = kwargs.get('school')
    school.start_class()


@admin_login_and_choose_school
def create_course(**kwargs):
    """创建课程"""
    school = kwargs.get('school')
    school.start_course()


@admin_login_and_choose_school
def display_school_students_info(**kwargs):
    school = kwargs.get('school', '')
    if not school:
        print('学校输入有误')
        return
    if not school.school_students:
        print('\033[1;35m对不起,该学校还未招收学生!\033[0m')
        return
    print('本校区学生信息如下'.center(30, '-'))
    print('姓名'.ljust(4, chr(12288)), '班级'.ljust(5), '成绩'.ljust(3))
    for student in school.school_students:
        info = student.__dict__
        class_name = Class.get_obj_by_id(info.get('class_id', '')).name
        print(info.get('name').ljust(4, chr(12288)), class_name.ljust(8), info.get('exam_result', ''))
    print(''.center(30, '-'))


@admin_login_and_choose_school
def display_school_courses_info(**kwargs):
    """显示本学校已经开设的课程信息"""
    school = kwargs.get('school')
    school.display_school_courses()


@admin_login_and_choose_school
def display_school_teachers_info(**kwargs):
    """显示本学校的教师信息"""
    school = kwargs.get('school')
    print()
    school.display_school_teachers()


@admin_login_and_choose_school
def display_school_classes_info(**kwargs):
    """显示本学校的班级信息"""
    school = kwargs.get('school')
    school_class_lst = school.school_classes
    if school_class_lst:
        school.display_school_classes()
        choice = input('查看班级信息(y)>>> ')
        if choice == 'y' or choice == 'yes':
            class_name = input('输入班级名称>>> ')
            if not Class.get_obj_by_name(class_name):
                print('对不起,您输入的班级名称有误')
                return
            class_obj = Class.get_obj_by_name(class_name)
            students_list = class_obj.class_students_info
            students_list = [student for student in students_list if student.active]
            if not students_list:
                print('目前本班级没有学生')
                return
            print('姓名'.ljust(6, chr(12288)), '性别'.ljust(4,chr(12288)), '联系方式'.ljust(8, chr(12288)), '地址'.ljust(20, chr(12288)))
            for student in students_list:
                print(format_print(student.name, 6), format_print(student.gender, 4),
                      format_print(student.mobile, 12), format_print(student.address, 20))
    else:
        print('\033[1;35m 目前为开设班级 \033[0m')
        return


@admin_login_build_school
def open_school(**kwargs):
    """调用装饰器函数登录并直接创建新校区"""
    pass


def show_all_login_students_detail():
    students = Student.get_all_objects()
    for student in students:
        print(student.__dict__)


