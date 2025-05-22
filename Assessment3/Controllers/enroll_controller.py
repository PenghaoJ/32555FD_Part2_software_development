from Assessment3.Moudels.student import Student  # 从 student.py 导入 Student 类
from Assessment3.Moudels.database import Database  # 从 database.py 导入 Database 类
from Assessment3.Moudels.subject import Subject  # 从 subject.py 导入 Subject 类
from Assessment3.Controllers.student_controller import AuthValidator  # 导入验证器类


class EnrollController:
    def __init__(self):
        self.db = Database()  # 使用 database.py 中的 Database 类

    def student_menu(self, student: Student):
        """
        学生系统界面：
        - 提供修改密码、选课、退课、查看成绩和退出系统的功能
        """
        while True:
            print("\n=== Student System ===")
            print("(c) Change Password")
            print("(e) Enroll in Courses (up to 4)")  # 选课功能
            print("(r) Drop Courses")  # 退课功能
            print("(s) View Grades and Scores")  # 查看成绩功能
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
        new_password = input("Enter new password: ")
        pwd_check = AuthValidator.validate_password(new_password)
        if not pwd_check['valid']:
            print("Password does not meet requirements:")
            for error in pwd_check['errors']:
                print(f"- {error}")
        else:
            student.password = new_password  # 更新明文密码
            print("Password updated successfully!")
            # 更新数据库中的密码
            students = self.db.load_all_students()
            for s in students:
                if s["name"] == student.name:
                    s["password"] = student.password
                    break
            self.db.save_all_students(students)

    def enroll_in_courses(self, student: Student):
        """
        选课功能：学生可以选择最多 4 门课程
        """
        if len(student.subjects) >= 4:
            print("You cannot enroll in more than 4 courses.")
            return

        course_name = input("Enter the course name to enroll: ")
        # 调用 student.py 中的 enrol_subject 方法
        if student.enrol_subject(course_name):
            print(f"Successfully enrolled in {course_name}.")
        else:
            print(f"You are already enrolled in {course_name}.")

        # 更新数据库
        self.update_student_in_database(student)

    def drop_courses(self, student: Student):
        """
        退课功能：学生可以从已选课程中退课
        """
        if not student.subjects:
            print("You are not enrolled in any courses.")
            return

        print("Your enrolled courses:")
        for i, subject in enumerate(student.subjects, start=1):
            # 修改显示格式为 序号.课程号-->课名
            print(f"{i}. {subject.id} --> {subject.name}")

        try:
            course_index = int(input("Enter the course number to drop: ")) - 1
            if 0 <= course_index < len(student.subjects):
                # 调用 student.py 中的 remove_subject_by_id 方法
                dropped_course = student.subjects[course_index]
                if student.remove_subject_by_id(dropped_course.id):
                    print(f"Successfully dropped {dropped_course.name}.")
                else:
                    print(f"Failed to drop {dropped_course.name}.")
            else:
                print("Invalid course number.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid course number.")
            return

        # 更新数据库
        self.update_student_in_database(student)

    def view_grades_and_scores(self, student: Student):
        """
        查看成绩和分数功能：显示学生已选课程及其成绩和等级
        """
        if not student.subjects:
            print("You have not enrolled in any courses.")
            return

        print("Your enrolled courses and grades:")
        for subject in student.subjects:
            # 确保每门课程都有成绩和等级
            mark = subject.mark if subject.mark is not None else "N/A"
            grade = subject.grade if subject.grade is not None else "N/A"
            print(f"[ Subject::{subject.name} -- mark = {mark} -- grade = {grade} ]")

    def update_student_in_database(self, student: Student):
        """
        更新学生信息到数据库
        """
        self.db.update_student(student)