import os
import json
from Assessment3.Moudels.student import Student
from Assessment3.Moudels.subject import Subject

class Database:
    FILE_PATH = "Assessment3/students.data"

    def __init__(self):
        if not os.path.exists(self.FILE_PATH):
            os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)
            with open(self.FILE_PATH, "w") as f:
                json.dump([], f)

    def load_all_students(self) -> list:
        students = []
        try:
            with open(self.FILE_PATH, "r") as f:
                for line in f:
                    if line.strip():
                        student_data = json.loads(line.strip())
                        # 将 subjects 字典列表转换为 Subject 对象
                        subjects = [
                            Subject(
                                name=subj["name"],
                                subj_id=subj["id"],
                                mark=subj["mark"],
                                grade=subj["grade"]
                            ) for subj in student_data["subjects"]
                        ]
                        # 创建 Student 对象并恢复数据
                        student = Student(
                            name=student_data["name"],
                            email=student_data["email"],
                            password=student_data["password"]
                        )
                        student.id = student_data["id"]
                        student.subjects = subjects
                        students.append(student.to_dict())
        except FileNotFoundError:
            pass
        return students

    def save_all_students(self, students: list):
        with open(self.FILE_PATH, "w") as f:
            for s in students:
                # 确保 subjects 是字典列表
                student_dict = s.copy()
                student_dict["subjects"] = [
                    subj.__dict__ for subj in s["subjects"]
                ]
                json_line = json.dumps(student_dict, ensure_ascii=False)
                f.write(json_line + "\n")

    def add_student(self, student: dict):
        students = self.load_all_students()
        students.append(student)
        self.save_all_students(students)

    def update_student(self, email: str, new_data: dict):
        """
        根据学生邮箱更新学生信息
        """
        students = self.load_all_students()  # 加载所有学生数据
        for i, s in enumerate(students):
            if s["email"] == email:  # 根据邮箱匹配
                students[i] = {**s, **new_data}  # 合并旧数据和新数据
                print(f"Student with email {email} has been updated.")
                break
        else:
            print(f"Student with email {email} not found. No update performed.")
        self.save_all_students(students)  # 保存更新后的学生数据

    def update_student_by_data(self, student_data):
        """
        根据学生数据更新学生信息
        """
        students = self.load_all_students()  # 加载所有学生数据
        for i, student in enumerate(students):
            if student["id"] == student_data["id"]:  # 根据学生 ID 匹配
                students[i] = student_data  # 更新学生数据
                break
        else:
            print(f"Student with ID {student_data['id']} not found. No update performed.")
        self.save_all_students(students)  # 保存更新后的学生数据

    def remove_student_by_id(self, student_id):
        """
        根据学生 ID 删除学生
        """
        students = self.load_all_students()  # 加载所有学生数据
        initial_count = len(students)
        students = [s for s in students if s["id"] != student_id]  # 过滤掉指定 ID 的学生
        if len(students) < initial_count:
            print(f"Student with ID {student_id} has been removed.")
        else:
            print(f"Student with ID {student_id} not found. No deletion performed.")
        self.save_all_students(students)  # 保存更新后的学生数据

# if __name__ == "__main__":
#     db = Database()
#     student = Student("Bob", "bob@university.com", "Pass123")
#     db.add_student(student)

#     all_students = db.load_all_students()
#     for s in all_students:
#         print(f"{s.name} - {s.email} - {s.get_pass_status()}")