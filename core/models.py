# -*- coding: utf-8 -*-   @Time    : 18-1-17 下午12:57
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com
import pickle
import re
from random import randint

from conf.settings import *
from lib.utils import create_id, hash_pwd
from core.logger import log_generate


class Base:
    """基类,用户继承属性"""
    def __init__(self, name):
        # 自定义id_属性, 唯一性
        self.id_ = create_id()
        self.name = name

    def save(self):
        """保存类对象至指定路径"""
        file_path = r'%s/%s' % (self.save_path, self.id_)
        with open(file_path, 'wb') as f:
            # 利用pickle方法保存python对象
            pickle.dump(self, f)

    @classmethod
    def get_all_objects(cls):
        """通过路径获取类的所有实例化对象,返回对象列表"""
        obj_lst = []
        obj_id_l = os.listdir(cls.save_path)
        for obj_id in obj_id_l:
            obj = pickle.load(open('%s/%s' % (cls.save_path, obj_id), 'rb'))
            obj_lst.append(obj)
        return obj_lst


    def __str__(self):
        """打印对象返回的信息"""
        res = ''
        for i in self.__dict__.items():
            res += i[0].ljust(20) + i[1] + '\n'
        # print('详细信息'.center(30, '>'))
        return res

    @classmethod
    def get_obj_by_name(cls, name):
        """类方法,通过name获取类的对象,"""
        id_l = os.listdir(cls.save_path)
        obj_lst = [pickle.load(open('%s/%s' % (cls.save_path, id), 'rb')) for id in id_l]
        target_obj = None
        for obj in obj_lst:
            if obj.name == name:
                target_obj = obj
                break
        return target_obj

    @classmethod
    def get_obj_by_id(cls, id_str):
        """类方法,通过id找到类的对象"""
        id_l = os.listdir(cls.save_path)
        obj_lst = [pickle.load(open('%s/%s' % (cls.save_path, _id), 'rb')) for _id in id_l]
        target_obj = None
        for obj in obj_lst:
            if obj.id_ == id_str:
                target_obj = obj
                break
        return target_obj


class School(Base):
    '''学校类, 兼顾创建班级,招收教师等接口'''
    save_path = SCHOOL_PATH

    def __init__(self):
        '''城市和具体地址'''
        if DEBUG:
            print('in School')
        print()
        print('创办学校中'.center(20, '-'))
        school_lst = School.get_all_objects()
        while True:
            # 1. 输入城市
            city = input('城市名称(q.返回主界面) >>> ').strip()
            if city == 'q':
                return
            if city not in MAIN_CITIES:
                print('\033[1;35m 对不起,该城市不在规划内 \033[0m')
            else:
                school_city_lst = [school.city for school in school_lst]
                if city not in school_city_lst:
                    print('\033[1;35m 对不起,该城市已经存在分校区 \033[0m')
                else:
                    # 2. 具体地址
                    address = input('学校地址 >>> ').strip()
                    # 初始化父类的属性
                    super().__init__('%s分校区' % city)
                    self.address = address
                    self.city = city
                    # 3. 保存新建的学校对象, 即调用父类的save方法保存至指定的路径
                    self.save()
                    print('学校建成'.center(20, '-'))
                    log_generate(log_type='admin', id='admin', message={
                        'type': '创办新校区', '城市': city, })
                    return

    def __str__(self):
        return '学校名称<{0}> 地址<{1}> {2}'.format(self.name, self.address, self.__dict__)

    def start_course(self):
        """开设课程"""
        Course(self)

    def start_class(self):
        """开设班级"""
        Class(self)

    def display_school_courses(self):
        """打印当前学校所有课程"""
        course_lst = self.school_courses
        if not course_lst:
            print('\033[1;35m 目前没有引进任何课程 \033[0m')
            return

        print('%s已开设课程如下'.center(30, '-') % self.name)
        print('name'.ljust(9), 'month'.ljust(8), 'price')
        for course in course_lst:
            print(str(course.name).ljust(9), str(course.learning_time).ljust(8), course.price)
        print(''.center(30, '-'))

    def display_school_classes(self):
        """显示当前学校所有班级"""
        if not self.school_classes:
            print('\033[1;35m该学校目前还未开班 \033[0m')
        else:
            print()
            print('校区班级列表'.center(20, '-'))
            print('%s已开设课程如下'.center(30, '-') % self.name)
            print('NAME'.ljust(14), 'MONTH'.ljust(8), 'TEACHER')
            for school_class in self.school_classes:
                class_course = Course.get_obj_by_id(school_class.course_id)
                class_teacher = Teacher.get_obj_by_id(school_class.teacher_id)
                print(str(school_class.name).ljust(14), class_course.name.ljust(8), class_teacher.name)
            print(''.center(20, '-'))

    def display_school_teachers(self):
        """显示当前学校所有老师"""
        school_teacher_lst = self.school_teachers
        if not school_teacher_lst:
            print('\033[1;35m目前未招收教师\033[0m')
            return
        else:
            print('%s的教师信息如下'.center(30, '-') % self.name)
            print('NAME'.ljust(10), 'GOOD_AT'.ljust(10), 'EXPERIENCE(year)')
            for school_teacher in school_teacher_lst:
                print(str(school_teacher.name).ljust(10),
                      str(school_teacher.teaching_course).ljust(10), int(school_teacher.teaching_years))
            print(''.center(20, '-'))

    @property
    def school_courses(self):
        """返回当前学校所有课程对象列表"""
        course_lst = []
        course_id_lst = os.listdir(Course.save_path)
        for course_id in course_id_lst:
            course = pickle.load(open('%s/%s' % (Course.save_path, course_id), 'rb'))
            if course.school_id == self.id_:
                course_lst.append(course)
        # if not course_lst:
        #     print('本学校未开设课程')
        return course_lst

    @property
    def school_classes(self):
        """返回当前学校所有班级对象列表"""
        school_class_lst = []
        school_class_id_lst = os.listdir(Class.save_path)
        for school_class_id in school_class_id_lst:
            school_class = pickle.load(open('%s/%s' % (Class.save_path, school_class_id), 'rb'))
            if school_class.school_id == self.id_:
                school_class_lst.append(school_class)
        return school_class_lst

    @property
    def school_teachers(self):
        """返回当前学校所有老师对象列表"""
        school_teacher_lst = []
        school_teacher_id_lst = os.listdir(Teacher.save_path)
        for teacher_id in school_teacher_id_lst:
            school_class = pickle.load(open('%s/%s' % (Teacher.save_path, teacher_id), 'rb'))
            if school_class.school_id == self.id_:
                school_teacher_lst.append(school_class)
        if not school_teacher_lst:
            print('对不起,本学校目前还未招收老师')
            return
        return school_teacher_lst

    @property
    def school_students(self):
        """返回当前学校所有学生对象列表"""
        school_student_lst = []
        school_student_id_lst = os.listdir(Student.save_path)
        for teacher_id in school_student_id_lst:
            school_student = pickle.load(open('%s/%s' % (Student.save_path, teacher_id), 'rb'))
            if school_student.school_id == self.id_:
                school_student_lst.append(school_student)
        return school_student_lst


class Teacher(Base):
    '''教师类'''
    save_path = TEACHER_PATH

    def __init__(self, school):
        print()
        print('招聘讲师中'.center(20, '-'))
        while True:
            # 1. 输入课程
            teaching_course = input('擅长课程(退出:q)>>> ').strip()
            if teaching_course == 'q':
                return
            if teaching_course not in HOT_COURSES :  # 只招收特定课程的教师
                print("对不起，您的课程不符合招聘要求['python', 'linux', 'go', 'java', 'php', 'c', 'c++']")

            else:
                # 2. 输入教龄
                teaching_years = input('经验(年) >>> ').strip()
                if not teaching_years.isdigit() or int(teaching_years) not in range(1, 50):
                    print('\033[1;35m对不起，我们招聘的教师至少需要2年工作经验 \033[0m')
                else:
                    while True:
                        # 3. 输入姓名
                        name = input('姓名(不能为空, 退出:q) >>> ').strip()
                        if name == 'q':
                            return

                        if school.school_teachers:
                            teacher_name_lst = [teacher.name for teacher in school.school_teachers if school.school_teachers]
                            if name in teacher_name_lst:
                                print('\033[1;35m 对不起,该教师已经招聘 \033[0m')
                                continue

                        # 4. 输入年龄, 性别
                        age = input('年龄(数字) >>> ').strip()
                        gender = input('性别(男|女) >>> ').strip()
                        if not name or not age.isdigit() or gender not in ('男', '女'):
                            print('\033[1;35m姓名或性别输入有误\033[0m')
                        else:
                            while True:
                                # 5. 输入密码
                                login_pwd = input('请输入您的登录密码(至少六位数)>>> ').strip()
                                if len(login_pwd) < 6 or not login_pwd.isalnum():
                                    print('\033[1;35m密码至少需要六位字母或数字 \033[0m')

                                else:
                                    # 6. 对象属性赋值及保存, 保存至对应的路径
                                    super().__init__(name)
                                    self.login_pwd = hash_pwd(login_pwd)
                                    self.school_id = school.id_
                                    self.age = age
                                    self.gender = gender
                                    self.teaching_course = teaching_course
                                    self.teaching_years = teaching_years
                                    print('招聘讲师成功'.center(20, '-'))
                                    self.save()
                                    log_generate(log_type='admin', id='admin', message={
                                        'type': '招收教师', '教师姓名': name, '性别': gender,
                                        '教授课程': teaching_course, '经验(年)': int(teaching_years)})
                                    return


class Course(Base):
    '''课程类'''
    save_path = COURSE_PATH

    def __init__(self, school):
        print()
        print('引进课程中'.center(20, '-'))
        while True:
            # 1. 输入课程名称
            course_name = input('课程名(退出q) >>> ').strip()
            if course_name == 'q':
                return

            if course_name not in HOT_COURSES:
                # 判断课程是否在规划范围内
                print('\033[1;35m此课程不在规划范围内 \033[0m')

            else:
                if course_name in [course.name for course in school.school_courses]:  # 判断是否重复创建
                    print('\033[1;35m 对不起,课程<%s>本校区已经创建 \033[0m' % course_name)

                else:
                    # 2. 学习时长, 收费
                    learning_time = input('学习时长(月) >>> ').strip()
                    price = input('收费(元) >>> ').strip()
                    if not learning_time.isdigit() or not price.isdigit():  # 输入合法性
                        print('\033[1;35m时间或价格输入有误 \033[0m')

                    else:
                        if int(learning_time) not in range(1, 13):
                            print('\033[1;35m学习时长应该保持在1-13个月 \033[0m')

                        else:
                            # 3. 保存对象至指定的路径
                            super().__init__(course_name)
                            self.school_id = school.id_
                            self.learning_time = learning_time
                            self.price = price
                            print('课程引进成功'.center(20, '-'))
                            print()
                            self.save()
                            log_generate(log_type='admin', id='admin', message={
                                'type': '课程引进', '课程名': course_name, '课程时长': learning_time})
                            return


class Class(Base):
    """班类"""
    save_path = CLASS_PATH

    def __init__(self, school):
        print()
        print('班级创建中'.center(20, '-'))
        if DEBUG:
            print('in Class')
        self.school_id = school.id_
        while True:
            if not school.school_courses:   # 判断本校是否有课程
                print('\033[1;35m 本小区目前未引进任何课程 \033[0m')
                return

            school.display_school_courses()
            # 1. 绑定课程
            course_name = input('请选择课程名称 >>> ').strip()
            if course_name not in [course.name for course in school.school_courses]:  # 筛选重复课程
                print('\033[1;35m该课程未引进,请重新选择\033[0m')

            else:
                self.course_id = Course.get_obj_by_name(course_name).id_
                course_teachers_lst = []
                for school_teacher in school.school_teachers:
                    if school_teacher.teaching_course == course_name:
                        course_teachers_lst.append(school_teacher)
                if not course_teachers_lst:  # 筛选擅长本课程的教师
                    print('\033[1;35m对不起,目前没有招收此课程的教师\033[0m')
                    return

                school.display_school_teachers()
                while True:
                    # 2. 指定班级教师
                    teacher_name = input('选择教师 >>> ').strip()
                    if not Teacher.get_obj_by_name(teacher_name):
                        print('\033[1;35m 教师姓名输入有误 \033[0m')

                    else:
                        if Teacher.get_obj_by_name(teacher_name).teaching_course == course_name:
                            self.teacher_id = Teacher.get_obj_by_name(teacher_name).id_
                            class_name = input('输入班级名称>>> ').strip()
                            if class_name not in [class_.name for class_ in school.school_classes]:
                                super().__init__(class_name)
                                print('班级创建成功'.center(20, '-'))
                                print()
                                self.save()
                                log_generate(log_type='admin', id='admin', message={
                                    'type': '成立班级', '课程名': course_name, '班级名': class_name, '班级教师': teacher_name})
                                return

                            else:
                                print('\033[1;35m 班级名重复 \033[0m')

                        else:
                            print('\033[1;35m您选择的教师不擅长本班级课程 \033[0m')

    @property
    def class_students_info(self):
        """打印学生信息,排除未激活的学生"""
        student_lst = Student.get_all_objects()
        class_students_lst = []
        if not student_lst:
            print('本校区目前没有招收学生')
            return
        for student in student_lst:
            if student.class_id == self.id_ and student.active == 1:
                class_students_lst.append(student)
        return class_students_lst


class Student(Base):
    """学生类创建"""
    save_path = STUDENT_PATH  # 类属性,保存类的对象的路径

    def __init__(self):
        print('\n'+'注册中'.center(20, '-'))
        #  取出所有学校对象
        school_lst = School.get_all_objects()
        if not school_lst:
            print('\033[1;35m 对不起,目前没有校区 \033[0m')
            return
        while True:
            print()
            print('分校列表'.center(30, '-'))
            print('学校名称'.ljust(10), '地址'.ljust(15))
            for school in school_lst:
                print(str(school.name).ljust(10), str(school.address).ljust(15))
            # 1. 选择学校
            school_name = input('请选择学校(退出:q)>>> ').strip()
            if school_name == 'q':  # 选择退出,返回主界面
                return
            if not School.get_obj_by_name(school_name):  # 判断学校名称输入是否有误
                print('\033[1;35m 学校名称输入有误,请重新输入 \033[0m')
            else:
                # 2. 取出学校对象
                school = School.get_obj_by_name(school_name)

                # 3. 取出学校的多有班级
                if not school.school_classes:
                    print('\033[1;35m 对不起,当前学校没有创建班级 \033[0m')
                else:
                    self.school_id = school.id_
                    school.display_school_classes()  # 展示班级列表
                    # 获取当前学习的所有班级
                    class_name_lst = [class_.name for class_ in school.school_classes]  # 班级名称列表
                    while True:
                        # 4. 选择要加入的班级
                        class_name = input('请选择班级 >>> ').strip()
                        if class_name not in class_name_lst:
                            print('\033[1;35m 班级名输入有误,请重新输入 \033[0m')

                        else:
                            # 5. 获取班级对象
                            class_ = Class.get_obj_by_name(class_name)
                            if not class_:  # 通过名称获取班级
                                print('\033[1;35m 班级名称有误,请重新输入 \033[0m')

                            else:
                                while True:
                                    # 6. 输入密码
                                    login_pwd = input('请设置登录密码(至少六位数)>>> ').strip()
                                    if len(login_pwd) < 6 or not login_pwd.isalnum():
                                        print('\033[1;35m密码至少需要六位字母或数字 \033[0m')
                                    else:
                                        self.login_pwd = hash_pwd(login_pwd)
                                        self.active = 0
                                        self.class_id = Class.get_obj_by_name(class_name).id_
                                        # 7. 输入姓名
                                        name = input('输入姓名(中文名字优先) >>> ').strip()
                                        # 判断是否存在重复姓名
                                        student_name_lst = [stu.name for stu in class_.class_students_info]
                                        if name in student_name_lst:
                                            print('\033[1;35m 学生姓名重复 \033[0m')
                                        else:
                                            # 8. 输入年龄和性别等信息
                                            age = input('年龄(必须为数字) >>> ').strip()
                                            gender = input('性别(男|女) >>> ').strip()
                                            if not name or gender not in ('男', '女') or not age.isdigit():
                                                print('\033[1;35m 名字,性别(male|female)或者年龄输入有误 \033[0m', end='\n\n')

                                            else:
                                                super().__init__(name)
                                                self.age = age
                                                self.gender = gender
                                                while True:
                                                    # 9. 输入联系方式
                                                    mobile = input('联系方式 >>> ').strip()
                                                    if not re.match('1[358]\d{9}', mobile):
                                                        print('\033[1;35m电话格式有误 \033[0m')
                                                    else:
                                                        self.mobile =  mobile
                                                        address = input('请输入您的住址>>> ').strip()
                                                        if not address:
                                                            print('\033[1;35m住址不能为空 \033[0m')
                                                        else:
                                                            self.address = address
                                                            print('%s同学,恭喜您注册成功!' % name)
                                                            print()
                                                            self.save()
                                                            log_generate(log_type='student', id=self.id_,
                                                                         message={'type': '注册', 'name': self.name,
                                                                                  'school': school.name,
                                                                                  'course': self.name,
                                                                                  'class': class_name,
                                                                                  'address': address})
                                                            return

    @property
    def final_exam_result(self):
        exam_result = randint(60, 100)
        return exam_result


if __name__ == '__main__':
    l = Teacher.get_all_objects()
    # for teacher in l:
    #     print(teacher.name, teacher.teaching_course, School.get_obj_by_id(teacher.school_id))