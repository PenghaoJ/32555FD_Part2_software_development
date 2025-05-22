import os
import pickle
from Assessment3.Moudels.student import Student

class Database:
    FILE_PATH = "students.data"

    def __init__(self):
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "wb") as f:
                pickle.dump([], f)

    def load_all_students(self):
        try:
            with open(self.FILE_PATH, "rb") as f:
                return pickle.load(f)
        except (EOFError, FileNotFoundError):
            return []

    def save_all_students(self, students):
        with open(self.FILE_PATH, "wb") as f:
            pickle.dump(students, f)

    def add_student(self, student):
        students = self.load_all_students()
        students.append(student)
        self.save_all_students(students)

    def remove_student_by_id(self, student_id):
        students = self.load_all_students()
        students = [s for s in students if s.id != student_id]
        self.save_all_students(students)

    def clear_database(self):
        self.save_all_students([])
        
    def update_student(self, student):
        """
        更新单个学生信息到数据库
        """
        students = self.load_all_students()
        for s in students:
            if s["name"] == student.name:
                # 更新学生的课程和其他信息
                s["subjects"] = [
                    {
                        "id": subject.id,
                        "name": subject.name,
                        "mark": subject.mark,
                        "grade": subject.grade
                    }
                    for subject in student.subjects
                ]
                s["password"] = student.password  # 更新密码（如果有修改）
                break
        self.save_all_students(students)

# if __name__ == "__main__":
#     db = Database()
#     student = Student("Bob", "bob@university.com", "Pass123")
#     db.add_student(student)

#     all_students = db.load_all_students()
#     for s in all_students:
#         print(f"{s.name} - {s.email} - {s.get_pass_status()}")