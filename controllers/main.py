import sys
import os

# 将项目根目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.student_controller import StudentController
from controllers.admin_controller import AdminController

def main():
    # 初始化学生控制器和管理员控制器
    student_controller = StudentController()
    admin_controller = AdminController()

    while True:
        # 主菜单
        print("\nUniversity Application System")
        print("(1) Register as Student")
        print("(2) Login as Student")
        print("(3) Admin Operations")
        print("(4) Exit")
        choice = input("Select an option: ")

        if choice == "1":
            # 学生注册
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            result = student_controller.register(name, email, password)
            print(result)
        elif choice == "2":
            # 学生登录
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            logged_in_student = student_controller.login(email, password)
            if isinstance(logged_in_student, str):
                # 登录失败，返回错误信息
                print(logged_in_student)
            else:
                # 登录成功，进入学生系统菜单
                student_menu(logged_in_student, student_controller)
        elif choice == "3":
            # 管理员操作菜单
            print("\nAdmin Operations")
            print("(1) Show all students")
            print("(2) Remove a student")
            print("(3) Clear all student data")
            admin_choice = input("Select an admin option: ")
            if admin_choice == "1":
                result = admin_controller.show_students()
                print("\n".join(result))
            elif admin_choice == "2":
                student_id = input("Enter the student ID to remove: ")
                result = admin_controller.remove_student(student_id)
                print(result)
            elif admin_choice == "3":
                result = admin_controller.clear_all_students()
                print(result)
            else:
                print("Invalid admin option.")
        elif choice == "4":
            # 退出系统
            print("Exiting the system...")
            break
        else:
            print("Invalid choice. Please try again.")

def student_menu(student, student_controller):
    # 学生系统菜单
    while True:
        print("\nStudent Menu")
        print("(1) Enroll in a subject")
        print("(2) Drop a subject")
        print("(3) View enrolled subjects")
        print("(4) Change password")
        print("(5) Logout")
        choice = input("Select an option: ")

        if choice == "1":
            # 选课
            subject_name = input("Enter the subject name to enroll: ")
            result = student.enrol_subject(subject_name)
            print(result)
        elif choice == "2":
            # 退课
            subject_id = input("Enter the subject ID to drop: ")
            result = student.remove_subject(subject_id)
            print(result)
        elif choice == "3":
            # 查看已选课程
            subjects = student.show_subjects()
            if isinstance(subjects, list):
                print("\n".join(subjects))
            else:
                print(subjects)
        elif choice == "4":
            # 修改密码
            old_password = input("Enter your current password: ")
            new_password = input("Enter your new password: ")
            result = student_controller.change_password(student, old_password, new_password)
            print(result)
        elif choice == "5":
            # 登出
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
