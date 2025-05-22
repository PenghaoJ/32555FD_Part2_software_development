from Controllers.student_controller import StudentLoginSystem
from Controllers.adminer_controller import AdminController 

def main():
    admin = AdminController()
    student_controller = StudentLoginSystem()

    print("Welcome to the Student Management System")
    while True:
        flag = input("University System:(A)dmin,(S)tudent,(E)xit: ")
        if flag.upper() == "A":
            admin.admin_menu()
        elif flag.upper() == "S": 
            student_controller.main()  # 调用 student_controller 的 main 方法
        elif flag.upper() == "E": 
            print("Exiting the system...")  
            break  # 退出循环
        else:
            print("Invalid choice. Please try again.")  # 输入无效时提示

if __name__ == "__main__":
    main()
