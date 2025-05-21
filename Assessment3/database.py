import os
import pickle
from student import Student

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

if __name__ == "__main__":
    db = Database()
    student = Student("Bob", "bob@university.com", "Pass123")
    db.add_student(student)

    all_students = db.load_all_students()
    for s in all_students:
        print(f"{s.name} - {s.email} - {s.get_pass_status()}")