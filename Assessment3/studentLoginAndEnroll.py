import re
import bcrypt
import json
from datetime import datetime

class Student:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = AuthValidator.hash_password(password)
        self.courses = []
        self.locked_until = None

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())


# 验证
class AuthValidator:
    @staticmethod
    def validate_email(email: str) :
        pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
        return bool(re.fullmatch(pattern, email))

    @staticmethod
    def validate_password(password: str) :
        errors = []
        if len(password) < 8:
            errors.append("length less than 8")
        if not re.search(r'[A-Z]', password):
            errors.append("empty majuscule")
        if not re.search(r'[a-z]', password):
            errors.append("empty minuscule")
        if not re.search(r'\d', password):
            errors.append("empty number")
        if not re.search(r'[\W_]', password):
            errors.append("empty specific symbol")
        return {"valid": len(errors) == 0, "errors": errors}

    @staticmethod
    def hash_password(password: str) :
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()




#异常

class AgainEnrollError(Exception):
    """重复注册异常"""
    def __init__(self, username):
        super().__init__(f" {username} is existing")

class EmailFormError(Exception):
    """邮箱格式异常"""
    def __init__(self, email):
        super().__init__(f" {email} form error")

class PasswordError(Exception):
    """密码异常"""
    def __init__(self, errors):
        super().__init__("your password " + ", ".join(errors))

class LoginExceededError(Exception):
    """登录尝试超限异常"""
    def __init__(self):
        super().__init__("Locked cause attempts too lot")


# 主体
class StudentLoginSystem:
    def __init__(self):
        self.students = {}
        self.login_attempts = {}

    def register(self, username: str, email: str, password: str):
        # 验证邮箱格式
        if not AuthValidator.validate_email(email):
            raise EmailFormError(email)

        # 验证密码强度
        pwd_check = AuthValidator.validate_password(password)
        if not pwd_check['valid']:
            raise PasswordError(pwd_check['errors'])

        # 检查重复注册
        if username in self.students:
            raise AgainEnrollError(username)

        self.students[username] = Student(username, email, password)
        return True

    def login(self, username: str, password: str) -> Student:
        # 检查账户锁定状态
        if username in self.login_attempts:
            last_attempt = self.login_attempts[username]
            if last_attempt['count'] >= 3:
                lock_time = last_attempt['lock_time']
                if (datetime.now() - lock_time).seconds < 1800:  # 30分钟锁定
                    raise LoginExceededError()

        # 验证用户信息
        if username not in self.students:
            raise ValueError("no search")

        student = self.students[username]
        if not student.check_password(password):
            # 记录登录尝试
            attempts = self.login_attempts.get(username, {'count': 0, 'lock_time': None})
            attempts['count'] += 1
            if attempts['count'] >= 3:
                attempts['lock_time'] = datetime.now()
            self.login_attempts[username] = attempts
            raise ValueError("Password error")

        # 重置登录尝试记录
        if username in self.login_attempts:
            del self.login_attempts[username]

        return student


# 显示
def main():
    system = StudentLoginSystem()

    while True:
        print("\n=== 学生系统 ===")
        print("1. Enroll")
        print("2. Login")
        print("3. Exit")
        choice = input("your choice: ")

        try:
            if choice == '1':
                username = input("Username: ")
                email = input("Email: ")
                password = input("Password: ")
                system.register(username, email, password)
                print("Success！")

            elif choice == '2':
                username = input("Username: ")
                password = input("Password: ")
                student = system.login(username, password)
                print(f"\n=== welcome! {student.username} ===")

            elif choice == '3':
                print("Byebye")
                break

        except Exception as e:
            print(f"Error: {str(e)}")

        finally:
            # 数据持久化示例（可扩展为文件存储）
            with open("students.json", "w") as f:
                data = {u: s.__dict__ for u, s in system.students.items()}
                json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()