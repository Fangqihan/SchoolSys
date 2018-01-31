# -*- coding: utf-8 -*-   @Time    : 18-1-19 下午9:47
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com

from core.models import *
from core.auth import *


@teacher_login_and_choose_class
def display_class_students_info(**kwargs):
    class_chosen = kwargs.get('class_chosen')
    print()
    print('学生成绩列表'.center(20, '-'))
    print('姓名'.ljust(4, chr(12288)), '班级'.ljust(13), '成绩'.ljust(3))
    for student in class_chosen.class_students_info:
        info = student.__dict__
        class_name = Class.get_obj_by_id(info.get('class_id', '')).name
        print(info.get('name').ljust(4, chr(12288)), class_name.ljust(15), info.get('exam_result', ''))
    print()


@teacher_login_and_choose_class
def change_class_students_info(**kwargs):
    print()
    print('修改学生成绩中'.center(20, '-'))
    teacher = kwargs.get('teacher')
    class_chosen = kwargs.get('class_chosen')
    name = input('请输入学生姓名>>>').strip()
    student = None

    for student_obj in class_chosen.class_students_info:
        if student_obj.name == name:
            student = student_obj
            break
    if not student:
        print('学生姓名输入有误')
        return
    student_exam_result = student.__dict__.get('exam_result', '')
    if DEBUG == True:
        print(student.__dict__)
    if not student_exam_result:
        print('该学生还未参加考试,请督促')
        print()
        return
    new_exam_result = input('输入新的分数>>> ')
    if not new_exam_result.isdigit():
        print('必须输入数字')
        return
    if not int(new_exam_result) in range(0, 101):
        print('对不起,分数在1和100之间')
        return
    student.exam_result = int(new_exam_result)
    print('分数修改修改成功'.center(20, '-'))
    log_generate(log_type='teacher', id=teacher.id_,
                 message={'操作类型': '修改学生成绩', '教师姓名': teacher.name,
                          '修改学生姓名': name, '班级名': class_chosen.name, '修改后成绩': new_exam_result})
    student.save()


