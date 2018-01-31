# -*- coding: utf-8 -*-   @Time    : 18-1-19 下午10:10
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com


from core.auth import *
from core.models import *


def student_enroll():
    """学生注册"""
    Student()


@student_login
def students_pay_tuition(**kwargs):
    student = kwargs.get('student')
    if student.active:
        print('\033[1;35m 您的账户已经是激活状态 \033[0m\n')
        return
    school_class = Class.get_obj_by_id(student.class_id)
    course = Course.get_obj_by_id(school_class.course_id)
    if not course:
        print('\033[1;35m 对不起,您选择的课程不存在 \033[0m',end='\n\n')
        return
    money = input('请缴纳学费%s元>>> ' % course.price)

    if not money.isdigit():
        print('\033[1;35m 输入金额必须为数字 \033[0m', end='\n\n')
        return
    elif int(money) < int(course.price):
        print('\033[1;35m 金额不够支付课程学费 \033[0m', end='\n\n')
        return
    student.active = 1
    student.save()
    print('%s同学, 恭喜您缴费激活成功!' % student.name)
    log_generate(log_type='student', id=student.id_,
                 message={'type': '激活', '学生姓名': student.name, '充值金额': money})


@student_login
def take_exam(**kwargs):
    student = kwargs.get('student')
    if student.__dict__.get('active','') == 0:
        print('\033[1;35m 对不起,您的账户未激活,请前往缴纳学费 \033[0m\n')
        return
    if student.__dict__.get('exam_result', ''):
        print('\033[1;35m不能重复考试 \033[0m\n')
        return
    result = student.final_exam_result
    student.exam_result = result
    class_obj = Class.get_obj_by_id(student.class_id)
    course = Course.get_obj_by_id(class_obj.course_id)

    student.save()
    print('\033[1;35m 考试完成，请静候成绩！ \033[0m', end='\n\n')
    log_generate(log_type='student', id=student.id_,
                 message={'操作类型': '考试', '学生姓名': student.name, '考试分数': result, '课程': course.name})
    input()



