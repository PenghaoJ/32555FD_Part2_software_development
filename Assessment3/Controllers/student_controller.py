import os
import sys

# 添加项目根目录到 sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, project_root)

import re
from datetime import datetime
from Assessment3.Moudels.student import Student  # 从 student.py 导入 Student 类
from Assessment3.Moudels.database import Database  # 从 database.py 导入 Database 类


# 验证器类
class AuthValidator:
    @staticmethod
    def validate_email(email: str):
        """
        验证邮箱格式是否正确。
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
        return bool(re.fullmatch(pattern, email))

    @staticmethod
    def validate_password(password: str):
        """
        验证密码是否符合要求：
        - 至少 8 个字符
        - 至少包含一个大写字母、一个小写字母、一个数字和一个特殊字符
        """
        errors = []
        if len(password) < 8:
            errors.append("Password length must be at least 8 characters.")
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number.")
        if not re.search(r'[\W_]', password):
            errors.append("Password must contain at least one special character.")
        return {"valid": len(errors) == 0, "errors": errors}


# 异常类
class AgainEnrollError(Exception):
    """重复注册异常"""
    def __init__(self, username_or_email):
        super().__init__(f"{username_or_email} is already existing")


class EmailFormError(Exception):
    """邮箱格式异常"""
    def __init__(self, email):
        super().__init__(f"{email} form error")


class PasswordError(Exception):
    """密码异常"""
    def __init__(self, errors):
        super().__init__("Password error: " + ", ".join(errors))


# 学生登录系统
class StudentLoginSystem:
    def __init__(self):
        self.db = Database()  # 使用 database.py 中的 Database 类

    def register(self, username: str, email: str, password: str):
        """
        注册新学生：
        - 验证邮箱格式
        - 验证密码强度
        - 检查用户名和邮箱是否已存在
        - 保存到数据库
        """
        if not AuthValidator.validate_email(email):
            raise EmailFormError(email)

        pwd_check = AuthValidator.validate_password(password)
        if not pwd_check['valid']:
            raise PasswordError(pwd_check['errors'])

        students = self.db.load_all_students()
        if any(s["name"] == username for s in students):
            raise AgainEnrollError(f"Username '{username}'")
        if any(s["email"] == email for s in students):
            raise AgainEnrollError(f"Email '{email}'")

        student = Student(username, email, password)
        students.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "password": student.password,  # 明文存储密码
            "subjects": student.subjects
        })
        self.db.save_all_students(students)
        return True

    def login(self, email: str, password: str) -> Student:
        """
        登录学生账户：
        - 从数据库加载学生数据
        - 验证邮箱和密码
        - 返回 Student 对象
        """
        students = self.db.load_all_students()
        student_data = next((s for s in students if s["email"] == email), None)
        if not student_data:
            raise ValueError("Email not found.")

        if student_data["password"] != password:  # 直接比较明文密码
            raise ValueError("Incorrect password.")

        return Student(
            name=student_data["name"],
            email=student_data["email"],
            password=student_data["password"]
        )

    def main(self):
        """
        学生系统主菜单
        """
        while True:
            print("\n=== Student Management System ===")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Your choice: ")

            try:
                if choice == '1':
                    username = input("Username: ")
                    email = input("Email: ")
                    password = input("Password: ")
                    self.register(username, email, password)
                    print("Registration successful!")

                elif choice == '2':
                    email = input("Email: ")  # 提示用户输入邮箱
                    password = input("Password: ")
                    student = self.login(email, password)  # 使用邮箱登录
                    print(f"\n=== Welcome, {student.name}! ===")

                    # 延迟导入 EnrollController
                    from Assessment3.Controllers.enroll_controller import EnrollController
                    enroll_controller = EnrollController()
                    enroll_controller.student_menu(student)  # 调用学生系统界面

                elif choice == '3':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")  # 输入无效时提示

            except Exception as e:
                print(f"Error: {str(e)}")