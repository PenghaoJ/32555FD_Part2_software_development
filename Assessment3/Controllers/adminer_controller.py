from Assessment3.Moudels.database import Database
from Assessment3.Moudels.student import Student


class AdminController:
    def __init__(self):
        self.db = Database()

    def clear_all_students(self):
        """
        清空所有学生数据
        """
        self.db.clear_database()
        print("All student data has been cleared.")

    def group_students_by_grades(self):
        """
        按成绩分组学生，并显示具体分数和评级
        """
        students = self.db.load_all_students()
        if not students:
            print("No students found.")
            return

        grade_groups = {}

        for student in students:
            for subject in student["subjects"]:
                grade = subject["grade"] or "N/A"
                mark = subject["mark"] if subject["mark"] is not None else "N/A"
                if grade not in grade_groups:
                    grade_groups[grade] = []
                grade_groups[grade].append({
                    "student_name": student["name"],
                    "student_id": student["id"],
                    "course_id": subject["id"],
                    "course_name": subject["name"],
                    "mark": mark,
                    "grade": grade
                })

        print("\n=== Students Grouped by Grades ===")
        for grade, entries in grade_groups.items():
            print(f"\nGrade {grade}:")
            for entry in entries:
                print(f"  - Student: {entry['student_name']} (ID: {entry['student_id']}), "
                      f"Course ID: {entry['course_id']}, Course Name: {entry['course_name']}, "
                      f"Mark: {entry['mark']}, Grade: {entry['grade']}")

    def classify_students_pass_fail(self):
        """
        将学生的每门课程划分为 PASS/FAIL 类别，并显示具体分数和评级
        """
        students = self.db.load_all_students()
        if not students:
            print("No students found.")
            return

        pass_courses = []
        fail_courses = []

        for student in students:
            for subject in student["subjects"]:
                mark = subject["mark"] if subject["mark"] is not None else "N/A"
                grade = subject["grade"] or "N/A"
                if grade == "F":
                    fail_courses.append({
                        "student_name": student["name"],
                        "student_id": student["id"],
                        "course_id": subject["id"],
                        "course_name": subject["name"],
                        "mark": mark,
                        "grade": grade
                    })
                else:
                    pass_courses.append({
                        "student_name": student["name"],
                        "student_id": student["id"],
                        "course_id": subject["id"],
                        "course_name": subject["name"],
                        "mark": mark,
                        "grade": grade
                    })

        print("\n=== PASS Courses ===")
        if pass_courses:
            for entry in pass_courses:
                print(f"  - Student: {entry['student_name']} (ID: {entry['student_id']}), "
                      f"Course ID: {entry['course_id']}, Course Name: {entry['course_name']}, "
                      f"Mark: {entry['mark']}, Grade: {entry['grade']}")
        else:
            print("No PASS courses.")

        print("\n=== FAIL Courses ===")
        if fail_courses:
            for entry in fail_courses:
                print(f"  - Student: {entry['student_name']} (ID: {entry['student_id']}), "
                      f"Course ID: {entry['course_id']}, Course Name: {entry['course_name']}, "
                      f"Mark: {entry['mark']}, Grade: {entry['grade']}")
        else:
            print("No FAIL courses.")

    def remove_student(self):
        """
        根据学生 ID 删除指定学生
        """
        students = self.db.load_all_students()
        if not students:
            print("No students available to delete.")
            return

        print("\n=== All Students ===")
        for student in students:
            print(f"ID: {student['id']}, Name: {student['name']} (Email: {student['email']})")

        while True:
            student_id = input("Enter the student ID to delete: ").strip()
            if not student_id:
                print("Student ID cannot be empty. Please try again.")
                continue

            student_to_remove = next((s for s in students if s["id"] == student_id), None)

            if student_to_remove:
                self.db.remove_student_by_id(student_id)
                print(f"Student {student_to_remove['name']} (ID: {student_id}) has been removed.")
                break
            else:
                print("Invalid student ID. Please try again.")

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
            print(f"Name: {student['name']} (ID: {student['id']}), Email: {student['email']}")
            print("Subjects:")
            for subject in student["subjects"]:
                mark = subject["mark"] if subject["mark"] is not None else "N/A"
                grade = subject["grade"] if subject["grade"] is not None else "N/A"
                print(f"  - {subject['name']} (ID: {subject['id']}, Mark: {mark}, Grade: {grade})")
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