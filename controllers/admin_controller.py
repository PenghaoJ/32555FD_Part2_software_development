from models.database import Database

class AdminController:
    def __init__(self):
        self.db = Database()

    def show_students(self):
        # 显示所有学生
        students = self.db.load_students()
        if not students:
            return "No students available."
        return [f"{student.id} - {student.name}, Email: {student.email}" for student in students]

    def remove_student(self, student_id):
        # 根据ID移除学生
        students = self.db.load_students()
        for student in students:
            if student.id == student_id:
                students.remove(student)
                self.db.save_students(students)
                return f"Student {student.name} removed."
        return "Student ID not found."

    def clear_all_students(self):
        # 清空所有学生数据
        self.db.save_students([])
        return "All student data cleared."
