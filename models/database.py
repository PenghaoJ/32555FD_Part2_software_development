import os
import pickle
from models.student import Student

class Database:
    FILE_PATH = "students.data"  # 数据文件路径

    def __init__(self):
        # 初始化数据库，如果文件不存在则创建
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "wb") as f:
                pickle.dump([], f)

    def load_students(self):
        # 从文件加载学生数据
        with open(self.FILE_PATH, "rb") as f:
            return pickle.load(f)

    def save_students(self, students):
        # 将学生数据保存到文件
        with open(self.FILE_PATH, "wb") as f:
            pickle.dump(students, f)

    def add_student(self, student):
        # 添加学生到数据库
        students = self.load_students()
        students.append(student)
        self.save_students(students)

    def find_student_by_email(self, email):
        # 根据邮箱查找学生
        students = self.load_students()
        for student in students:
            if student.email == email:
                return student
        return None
