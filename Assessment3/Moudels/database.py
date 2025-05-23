import os
import json
from Assessment3.Moudels.student import Student

class Database:
    FILE_PATH = "students.data"

    def __init__(self):
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w") as f:
                f.write("")

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
        students = self.load_all_students()
        for i, s in enumerate(students):
            if s["email"] == email:
                students[i] = {**s,  ** new_data}
                break
        self.save_all_students(students)

# if __name__ == "__main__":
#     db = Database()
#     student = Student("Bob", "bob@university.com", "Pass123")
#     db.add_student(student)

#     all_students = db.load_all_students()
#     for s in all_students:
#         print(f"{s.name} - {s.email} - {s.get_pass_status()}")