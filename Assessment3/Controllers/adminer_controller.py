from Assessment3.Moudels.database import Database
from Assessment3.Moudels.student import Student

class AdminController:
    def __init__(self):
        self.db = Database()  # 初始化数据库对象

    def clear_all_students(self):
        """
        清空所有学生数据
        """
        self.db.clear_database()
        print("All student data has been cleared.")

    def group_students_by_grades(self):
        """
        按成绩分组学生
        """
        students = self.db.load_all_students()
        grade_groups = {}

        for student in students:
            for subject in student["subjects"]:
                grade = subject["grade"] or "N/A"  # 如果没有成绩，使用 "N/A"
                if grade not in grade_groups:
                    grade_groups[grade] = []
                grade_groups[grade].append({
                    "student_name": student["name"],
                    "course_id": subject["id"],
                    "course_name": subject["name"]
                })

        print("\n=== Students Grouped by Grades ===")
        for grade, entries in grade_groups.items():
            print(f"\nGrade {grade}:")
            for entry in entries:
                print(f"{entry['student_name']}:{entry['course_id']}-->{entry['course_name']}") 

    def classify_students_pass_fail(self):
        """
        将学生的每门课程划分为 PASS/FAIL 类别，并显示课程 ID 和课程名
        """
        students = self.db.load_all_students()
        pass_courses = []
        fail_courses = []

        for student in students:
            for subject in student["subjects"]:
                if subject["grade"] == "F":  # 如果等级是 F，则归为 FAIL
                    fail_courses.append({
                        "student_name": student["name"],
                        "course_id": subject["id"],
                        "course_name": subject["name"],
                        "grade": subject["grade"]
                    })
                else:  # 其他等级归为 PASS
                    pass_courses.append({
                        "student_name": student["name"],
                        "course_id": subject["id"],
                        "course_name": subject["name"],
                        "grade": subject["grade"]
                    })

        print("\n=== PASS Courses ===")
        if pass_courses:
            for entry in pass_courses:
                print(f"  - Student: {entry['student_name']}, Course ID: {entry['course_id']}, "
                      f"Course Name: {entry['course_name']}, Grade: {entry['grade']}")
        else:
            print("No PASS courses.")

        print("\n=== FAIL Courses ===")
        if fail_courses:
            for entry in fail_courses:
                print(f"  - Student: {entry['student_name']}, Course ID: {entry['course_id']}, "
                      f"Course Name: {entry['course_name']}, Grade: {entry['grade']}")
        else:
            print("No FAIL courses.")

    def remove_student(self):
        """
        删除指定学生
        """
        students = self.db.load_all_students()
        if not students:
            print("No students available to delete.")
            return

        print("\n=== All Students ===")
        for i, student in enumerate(students, start=1):
            print(f"{i}:{student['id']} {student['name']} (Email: {student['email']})")

        try:
            student_index = int(input("Enter the student number to delete: ")) - 1
            if 0 <= student_index < len(students):
                student_id = students[student_index]["id"]
                self.db.remove_student_by_id(student_id)
                print(f"Student {students[student_index]['name']} has been removed.")
            else:
                print("Invalid student number.")
        except ValueError:
            print("Invalid input. Please enter a valid student number.")

    def display_all_students(self):
        """
        显示所有学生数据
        """
        students = self.db.load_all_students()
        if not students:
            print("No students found.")
            return

        print("\n=== All Students ===")
        for student in students:
            print(f"Name: {student['name']}, Email: {student['email']}")
            print("Subjects:")
            for subject in student["subjects"]:
                mark = subject["mark"] if subject["mark"] is not None else "N/A"
                grade = subject["grade"] if subject["grade"] is not None else "N/A"
                print(f"  - {subject['name']} (Mark: {mark}, Grade: {grade})")
            print("-" * 40)

    def admin_menu(self):
        """
        管理员子系统主菜单
        """
        while True:
            print("\n=== Admin System ===")
            print("(c) Clear all student data")
            print("(g) Group students by grades")
            print("(p) Classify students as PASS/FAIL")
            print("(r) Remove a student")
            print("(s) Show all student data")
            print("(x) Exit")
            choice = input("Your choice: ").lower()

            if choice == "c":
                self.clear_all_students()
            elif choice == "g":
                self.group_students_by_grades()
            elif choice == "p":
                self.classify_students_pass_fail()
            elif choice == "r":
                self.remove_student()
            elif choice == "s":
                self.display_all_students()
            elif choice == "x":
                print("Exiting Admin System...")
                break
            else:
                print("Invalid choice. Please try again.")