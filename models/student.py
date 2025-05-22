import random
from models.subjects import Subject

class Student:
    used_ids = set()  # 用于存储已生成的唯一ID

    def __init__(self, name, email, password):
        self.id = self.generate_id()  # 唯一的6位学生ID
        self.name = name  # 学生姓名
        self.email = email  # 学生邮箱
        self.password = password  # 学生密码
        self.subjects = []  # 学生已选课程列表

    def generate_id(self):
        # 确保生成的ID唯一
        while True:
            new_id = f"{random.randint(1, 999999):06d}"  # 生成6位随机ID
            if new_id not in Student.used_ids:  # 检查是否已存在
                Student.used_ids.add(new_id)  # 添加到已使用ID集合
                return new_id

    def enrol_subject(self, subject_name):
        # 学生选课
        if len(self.subjects) >= 4:
            return 'Cannot enroll in more than 4 subjects.'
        new_subject = Subject(subject_name)
        self.subjects.append(new_subject)
        return f'Enrolled in {subject_name} with mark {new_subject.mark}.'

    def remove_subject(self, subject_id):
        # 学生退课
        for subject in self.subjects:
            if subject.id == subject_id:
                self.subjects.remove(subject)
                return f'Removed subject {subject.name}.'
        return 'Subject ID not found.'

    def show_subjects(self):
        # 显示学生已选课程
        if not self.subjects:
            return 'No subjects enrolled.'
        return [f"{sub.id} - {sub.name}: {sub.mark} ({sub.grade})" for sub in self.subjects]
