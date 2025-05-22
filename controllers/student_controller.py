import re
import bcrypt
from models.student import Student
from models.database import Database

class AuthValidator:
    @staticmethod
    def validate_email(email: str):
        # 验证邮箱格式
        pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
        return bool(re.fullmatch(pattern, email))

    @staticmethod
    def validate_password(password: str):
        # 验证密码格式
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number.")
        if not re.search(r'[^\w]', password):
            errors.append("Password must contain at least one special character.")
        return {"valid": len(errors) == 0, "errors": errors}

    @staticmethod
    def hash_password(password: str):
        # 对密码进行哈希加密
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

class StudentController:
    def __init__(self):
        self.db = Database()

    def register(self, name, email, password):
        # 学生注册逻辑
        if not AuthValidator.validate_email(email):
            return "Invalid email format."
        password_validation = AuthValidator.validate_password(password)
        if not password_validation["valid"]:
            return f"Password errors: {', '.join(password_validation['errors'])}"
        if self.db.find_student_by_email(email):
            return "Email is already registered."
        hashed_password = AuthValidator.hash_password(password)
        new_student = Student(name, email, hashed_password)
        self.db.add_student(new_student)
        return "Registration successful."

    def login(self, email, password):
        # 学生登录逻辑
        student = self.db.find_student_by_email(email)
        if not student:
            return "Student not found."
        if bcrypt.checkpw(password.encode(), student.password.encode()):
            return f"Welcome back, {student.name}!"
        return "Invalid password."
