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
        # All groups use this to read current student records

    def save_all_students(self, students):
        with open(self.FILE_PATH, "wb") as f:
            pickle.dump(students, f)
        # Internal use, used automatically by add/remove/etc.

    def add_student(self, student):
        students = self.load_all_students()
        students.append(student)
        self.save_all_students(students)
        # Group B: Called after registration

    def remove_student_by_id(self, student_id):
        students = self.load_all_students()
        students = [s for s in students if s.id != student_id]
        self.save_all_students(students)
        # Group D: Called from admin interface

    def clear_database(self):
        self.save_all_students([])
        # Group D: Used to clear all student records
