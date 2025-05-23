import random


class Subject:
    # 用于存储已生成的 ID，确保不重复
    generated_ids = set()

    def __init__(self, name, subj_id=None, mark=None, grade=None):
        self.id = subj_id if subj_id else self.generate_id()
        self.name = name
        self.mark = mark if mark is not None else random.randint(25, 100)
        self.grade = grade if grade else self.calculate_grade()

    def generate_id(self):
        """
        生成一个随机的三位不重复 ID。
        如果生成的 ID 已存在，则重新生成，直到生成唯一的 ID。
        """
        while True:
            new_id = f"{random.randint(1, 999):03d}"  # 生成三位随机数并补零
            if new_id not in Subject.generated_ids:
                Subject.generated_ids.add(new_id)  # 将新生成的 ID 添加到集合中
                return new_id

    def calculate_grade(self):
        if self.mark >= 85:
            return "HD"
        elif self.mark >= 75:
            return "D"
        elif self.mark >= 65:
            return "C"
        elif self.mark >= 50:
            return "P"
        else:
            return "F"


# if __name__ == "__main__":
#     subject_list = [
#         "Programming Fundamentals",
#         "Data Structures",
#         "Algorithms",
#         "Software Engineering"
#     ]

#     for name in subject_list:
#         s = Subject(name)
#         print(f"Subject: {s.name}, ID: {s.id}, Mark: {s.mark}, Grade: {s.grade}")
