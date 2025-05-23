from Assessment3.Moudels.subject import Subject
import random

class Student:
    # 类变量，用于存储已生成的 ID，确保不重复
    generated_ids = set()

    def __init__(self, name, email, password, subjects=None):
        self.id = self.generate_id()
        self.name = name
        self.email = email
        self.password = password
        self.subjects = subjects or []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": [subj.__dict__ for subj in self.subjects]
        }

    def generate_id(self):
        """
        生成一个随机的六位不重复 ID。
        如果生成的 ID 已存在，则重新生成，直到生成唯一的 ID。
        """
        while True:
            new_id = f"{random.randint(1, 999999):06d}"  # 生成六位随机数并补零
            if new_id not in Student.generated_ids:
                Student.generated_ids.add(new_id)  # 将新生成的 ID 添加到类变量集合中
                return new_id

    def enrol_subject(self, course_name: str) -> bool:
        """
        添加课程到学生的课程列表。
        :param course_name: 课程名称
        :return: True 表示添加成功，False 表示课程已存在
        """
        # 检查课程是否已存在
        if any(subject.name == course_name for subject in self.subjects):
            return False  # 课程已存在

        # 如果课程不存在，则创建新课程并添加到列表
        new_subject = Subject(course_name)
        self.subjects.append(new_subject)
        return True

    def remove_subject_by_id(self, subject_id: str) -> bool:
        """
        根据课程 ID 从学生的课程列表中移除课程。
        :param subject_id: 课程 ID
        :return: True 表示移除成功，False 表示课程不存在
        """
        for subject in self.subjects:
            if subject.id == subject_id:
                self.subjects.remove(subject)
                return True  # 移除成功
        return False  # 课程不存在

    def get_average_mark(self):
        if not self.subjects:
            return 0
        return round(sum(s.mark for s in self.subjects) / len(self.subjects), 2)

    def get_pass_status(self):
        return "PASS" if self.get_average_mark() >= 50 else "FAIL"

    def change_password(self, new_password):
        self.password = new_password

    def get_subjects(self):
        return self.subjects

    def get_id(self):
        return self.id


# if __name__ == "__main__":
#     student = Student("Alice", "alice@university.com", "Password123")
#     print(f"Student ID: {student.id}")
#     print(f"Name: {student.name}")
#     print(f"Email: {student.email}")
#     print(f"Password: {student.password}")
#     student.enrol_subject("Programming Fundamentals")
#     student.enrol_subject("Data Structures")
#     student.enrol_subject("AI")
#     student.enrol_subject("Maths")
#     print("--- Subject List ---")
#     for subj in student.subjects:
#         print(f"{subj.name} - Mark: {subj.mark}, Grade: {subj.grade}")
#     print("Average:", student.get_average_mark())
#     print("Pass status:", student.get_pass_status())
