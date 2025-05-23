from Assessment3.Moudels.student import Student  # 从 student.py 导入 Student 类
from Assessment3.Moudels.database import Database
from Assessment3.Moudels.subject import Subject
from Assessment3.Controllers.student_controller import AuthValidator


class EnrollController:
    def __init__(self):
        self.db = Database()

    def student_menu(self, student: Student):
        """
        学生系统界面
        """
        while True:
            print("\n=== Student System ===")
            print("(c) Change Password")
            print("(e) Enroll in Courses (up to 4)")
            print("(r) Drop Courses")
            print("(s) View Grades and Scores")
            print("(x) Exit System")
            choice = input("Your choice: ").lower()

            if choice == 'c':
                self.change_password(student)
            elif choice == 'e':
                self.enroll_in_courses(student)
            elif choice == 'r':
                self.drop_courses(student)
            elif choice == 's':
                self.view_grades_and_scores(student)
            elif choice == 'x':
                print("Exiting student system...")
                break
            else:
                print("Invalid choice. Please try again.")

    def change_password(self, student: Student):
        """
        修改密码功能
        """
        print(f"\n=== Change Password for {student.name} (ID: {student.id}) ===")
        current_password = student.password

        while True:
            new_password = input("Enter new password: ").strip()
            confirm_password = input("Confirm new password: ").strip()

            if not new_password or not confirm_password:
                print("Password cannot be empty. Please try again.")
                continue

            if new_password != confirm_password:
                print("Passwords do not match. Please try again.")
                continue

            if new_password == current_password:
                print("New password cannot be the same as the current password. Please try again.")
                continue

            pwd_check = AuthValidator.validate_password(new_password)
            if not pwd_check['valid']:
                print("Password does not meet requirements:")
                for error in pwd_check['errors']:
                    print(f"- {error}")
                continue

            student.password = new_password
            print("Password updated successfully!")
            self.update_student_in_database(student)
            break

    def enroll_in_courses(self, student: Student):
        """
        选课功能
        """
        print(f"\n=== Enroll in Courses for {student.name} (ID: {student.id}) ===")
        if len(student.subjects) >= 4:
            print("You cannot enroll in more than 4 courses.")
            return

        while True:
            course_name = input("Enter the course name to enroll: ").strip()
            if not course_name:
                print("Course name cannot be empty. Please try again.")
                continue

            if student.enrol_subject(course_name):
                print(f"Successfully enrolled in {course_name}.")
                self.update_student_in_database(student)
                break
            else:
                print(f"You are already enrolled in {course_name}. Please try a different course.")

    def drop_courses(self, student: Student):
        """
        退课功能
        """
        print(f"\n=== Drop Courses for {student.name} (ID: {student.id}) ===")
        if not student.subjects:
            print("You are not enrolled in any courses.")
            return

        print("Your enrolled courses:")
        for subject in student.subjects:
            print(f"[ Course ID: {subject.id} | Subject: {subject.name} ]")

        while True:
            course_id = input("Enter the course ID to drop: ").strip()
            if not course_id:
                print("Course ID cannot be empty. Please try again.")
                continue

            dropped_course = next((subject for subject in student.subjects if subject.id == course_id), None)
            if dropped_course:
                if student.remove_subject_by_id(dropped_course.id):
                    print(f"Successfully dropped {dropped_course.name}.")
                    self.update_student_in_database(student)
                    break
                else:
                    print(f"Failed to drop {dropped_course.name}. Please try again.")
            else:
                print("Invalid course ID. Please try again.")

    def view_grades_and_scores(self, student: Student):
        """
        查看成绩和分数功能
        """
        print(f"\n=== Grades and Scores for {student.name} (ID: {student.id}) ===")
        if not student.subjects:
            print("You have not enrolled in any courses.")
            return

        for subject in student.subjects:
            mark = subject.mark if subject.mark is not None else "N/A"
            grade = subject.grade if subject.grade is not None else "N/A"
            print(f"[ Course ID: {subject.id} | Subject: {subject.name} -- Mark: {mark} -- Grade: {grade} ]")

    def update_student_in_database(self, student: Student):
        """
        更新学生信息到数据库
        """
        student_data = {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "password": student.password,
            "subjects": [{"id": subj.id, "name": subj.name, "mark": subj.mark, "grade": subj.grade} for subj in student.subjects]
        }
        self.db.update_student_by_data(student_data)