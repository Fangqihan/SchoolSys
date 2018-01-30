
# 模拟学校内部系统

---
## 主要功能如下:
> 学生相关操作:
1. 报名注册
2. 缴费激活账号(需登录认证)
3. 考试(需登录认证且账号激活激活)

> 教师相关操作:
1. 查看本班级信息(需登录认证)
2. 修改班级学员成绩(需登录认证)

> 系统管理员操作:
1. 引进课程:需要在规划范围内,在设置文件中有课程规划范围
2. 招收讲师
3. 成立班级
4. 本校课程信息
5. 本校班级信息
6. 本校老师信息
7. 本校学生信息
8. 新建学校

---

## 代码结构分布图
![项目目录](http://oyhijg3iv.bkt.clouddn.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE_%E9%80%89%E6%8B%A9%E5%8C%BA%E5%9F%9F_20180120163618.png)

## 项目包详细说明
1. start.py
 * 文件为程序主入口, 包含了程序的所有功能,可以直接调用 core包的功能函数,

2. core/auth.py
 * 用户登录函数: 分为学生身份认证,教师身份认证和管理员身份认证,其中管理员的具体设定信息在conf.setting.py 文件中设置;

 * 登出函数 logout(): 仅退出当前账号的登录,随后返回主界面,进行后续操作需要重新登录. 在管理模式下创建新学校后会重新登录.

3. core/admin_operations.py,student_operations.py,teacher_operations功能操作函数接口
	* 分别管理员,学生和教师操作的应用接口

4. core/models.py
 * 系统所有涉及的类的定义文件,**注意:在主界面都是通过接口函数与这些类互动,没有直接被调用!**

5. core/logger.py.py
 * 日志文件设置,主要分为students, teacher和 admin三种文件记录,在用户操作完成后调用log_generate函数即可将信息输入到对应的日志文件

---

## 操作提示
* 系统设定的admin用户见conf.setting.py文件,可以直接修改,初始账号:lynnfang,初始密码:fqh202.
* 之前的调试增加的所有学生或教师的登录密码都经过加密,初始密码为 abc123.
* 武汉分校区最先创建,信息最全面,以供迅速了解

## 增加功能
* 若db目录下未生成任何对象,那么以管理员模式登录,创建的前后顺序如下:
    1. 新建学校对象
