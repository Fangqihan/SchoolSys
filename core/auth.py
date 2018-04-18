# -*- coding: utf-8 -*-   @Time    : 18-1-19 下午10:29
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com

from core.models import *
from core.admin_functions import *

student_login_status = False
student_online = None
teacher_login_status = False
teacher_online = None
teacher_class_chosen = None

admin_login_status = False
admin_school_chosen = ''


def teacher_login_and_choose_class(func):
    """教师身份验证装饰器函数"""
    def inner():
        global teacher_login_status
        global teacher_online
        global teacher_class_chosen
        if teacher_login_status == 1:
            return func(teacher=teacher_online, class_chosen=teacher_class_chosen)

        print('教师登录中'.center(20, '-'))
        # 1. 输入姓名
        name = input('输入您的姓名>>> ').strip()
        teacher = Teacher.get_obj_by_name(name)
        if not teacher:
            print('\033[1;35m姓名输入有误 \033[0m')
            return
        # 2. 输入密码
        password = input('输入您的验证密码>>> ').strip()
        password = hash_pwd(password)
        if teacher.login_pwd != password:
            print('\033[1;35m对不起,密码输入有误 \033[0m\n')
            return
        print('登录成功'.center(20, '-'))
        print()
        # 3. 登录成功修改状态
        teacher_login_status = 1
        teacher_online = teacher
        log_generate(log_type='teacher', id=teacher_online.id_,
                     message={'操作类型': '登录', '姓名': teacher_online.name})

        classes = Class.get_all_objects()  # 获取所有的班级
        if not classes:
            print('\033[1;35m该校区目前没有开班\033[0m')
            teacher_logout()
            return

        # 4. 找到与此老师绑定的班级
        teacher_classes_lst = [teacher_class for teacher_class in classes if teacher_class.teacher_id == teacher.id_]
        if not teacher_classes_lst:
            print('\033[1;35m该教师没有指定教学班级 \033[0m')
            teacher_logout()
            return

        print('NAME'.ljust(14), 'COURSE')
        for teacher_class in teacher_classes_lst:
            course = Course.get_obj_by_id(teacher_class.course_id)
            print(teacher_class.name.ljust(14), course.name)
        print(''.ljust(30, '-'))

        while True:
            # 4. 选择上课班级
            class_name = input('请选择上课班级(输入班级全称)>>> ').strip()  # 输入班级名称
            class_name_lst = [class_.name for class_ in teacher_classes_lst]
            class_chosen = Class.get_obj_by_name(class_name)
            if class_name not in class_name_lst or not class_chosen:
                print('\033[1;35m班级输入有误\033[0m')

            else:
                global teacher_class_chosen
                teacher_class_chosen = class_chosen
                log_generate(log_type='teacher', id=teacher.id_,
                             message={'操作类型': '选择上课班级', '姓名': teacher.name,
                                      '班级名': teacher_class_chosen.name})
                return func(teacher=teacher_online, class_chosen=teacher_class_chosen)

    return inner


def teacher_logout():
    global teacher_online
    global teacher_class_chosen
    global teacher_login_status
    if teacher_online:
        log_generate(log_type='teacher', id=teacher_online.id_,
                     message={'操作类型': '退出登录', '姓名': teacher_online.name})
    teacher_online = None
    teacher_class_chosen = None
    teacher_login_status = 0


def student_login(func):
    """学生登录验证"""
    def inner(**kwargs):
        global student_login_status
        global student_online
        if not student_login_status:
            print()
            print('登录中'.center(20, '-'))
            name = input('输入您的姓名>>> ').strip()
            student = Student.get_obj_by_name(name)
            if student:  # 通过学生姓名获取到学生对象
                count = 0
                while True:
                    password = input('输入您的注册密码>>> ').strip()
                    password = hash_pwd(password)
                    if student.login_pwd == password:
                        student_login_status = 1
                        print()
                        print('登录成功'.center(20, '-'))
                        student_online = student
                        return func(student=student_online)
                    print('\033[1;35m 密码输入有误 \033[0m', end='\n\n')
                    count += 1
                    if count == 3:
                        student.lock_status = 1
                        student.save()
                        print('\033[1;35m 对不起,您的账户因为输入次数过多已经冻结 \033[0m')
                        break


            else:
                print('\033[1;35m 姓名输入有误 \033[0m', end='\n\n')


        else:
            return func(student=student_online)

    return inner


def student_logout():
    global student_online
    global student_login_status
    if student_login_status:
        log_generate(log_type='student', id=student_online.id_,
                     message={'操作类型': '退出登录', '姓名': student_online.name})
        student_login_status = 0
        student_online = None
    print()


def admin_login_and_choose_school(func):
    """管理员登录身份验证, 选择学校或者建立新的校区"""
    def inner():
        global admin_login_status
        if admin_login_status == 1:
            return func(school=admin_school_chosen)

        print('管理员登录中'.center(20, '-'))
        # 1. 输入用户名和密码
        username = input('管理账户名>>> ').strip()
        password = input('密码 >>> ').strip()
        if username != ADMIN_ACCOUNT['username']:
            print('\033[1;35m用户名输入有误 \033[0m\n')
            return
        if password != ADMIN_ACCOUNT['password']:
            print('\033[1;35m密码有误! \033[0m\n')
            return
        print('登录成功'.center(22, '-'), end='\n\n')
        log_generate(log_type='admin', id='admin',
                     message={'type': '登录'})
        admin_login_status = 1

        global admin_school_chosen
        if admin_school_chosen:
            return func(school=admin_school_chosen)

        school_lst = School.get_all_objects()
        if not school_lst:
            new_school = School()
            admin_school_chosen = new_school
            return func(school=admin_school_chosen)

        display_schools_info()  # 打印学校列表(名称和地址)
        while True:
            #  1. 选择登录的学校
            school_name = input('请选择学校(输入学校全称) >>> ').strip()
            for school in school_lst:
                if school.name == school_name:
                    admin_school_chosen = school

            if admin_school_chosen:
                log_generate(log_type='admin', id='admin',
                             message={'type': '选择校区', 'school_chosen': admin_school_chosen.name})
                return func(school=admin_school_chosen)
            else:
                print('\033[1;35m输入有误,请确认后重新输入\033[0m')

    return inner


def admin_login_build_school(func):
    """管理员登录装饰器函数"""
    def inner():
        global admin_login_status
        if admin_login_status == 0:
            print()
            print('管理员登录中'.center(20, '-'))
            while True:
                username = input('管理账户名>>> ')
                password = input('密码 >>> ')
                if username != ADMIN_ACCOUNT['username']:
                    print('\033[1;35m用户名输入有误 \033[0m\n')
                    return
                if password != ADMIN_ACCOUNT['password']:
                    print('\033[1;35m密码有误! \033[0m\n')
                    return
                print('登录成功'.center(20, '-'), end='\n\n')
                log_generate(log_type='admin', id='admin',
                             message={'type': '登录'})
                admin_login_status = 1
                # 创建新校区
                global admin_school_chosen
                new_school = School()
                admin_school_chosen = new_school
                return func(school=admin_school_chosen)

        else:
            # 创建新校区
            new_school = School()
            admin_school_chosen = new_school
            return func(school=admin_school_chosen)

    return inner


def admin_logout():
    global admin_login_status
    global admin_school_chosen
    if admin_login_status:
        log_generate(log_type='admin', id='admin',
                     message={'操作类型': '退出登录'})
    admin_login_status = 0
    admin_school_chosen = None
    print('退出登录'.center(20, '-'))
    print()