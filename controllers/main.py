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
            result = student_controller.login(email, password)
            print(result)
        elif choice == "3":
            # 管理员操作菜单
            print("\nAdmin Operations")
            print("(1) Show all students")
            print("(2) Remove a student")
            print("(3) Clear all student data")
            admin_choice = input("Select an admin option: ")
            if admin_choice == "1":
                # 显示所有学生
                result = admin_controller.show_students()
                print("\n".join(result))
            elif admin_choice == "2":
                # 移除学生
                student_id = input("Enter the student ID to remove: ")
                result = admin_controller.remove_student(student_id)
                print(result)
            elif admin_choice == "3":
                # 清空所有学生数据
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

if __name__ == "__main__":
    main()
