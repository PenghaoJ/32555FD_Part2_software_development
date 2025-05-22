import random

class Subject:
    used_ids = set()  # 用于存储已生成的唯一ID

    def __init__(self, name):
        self.id = self.generate_id()  # 唯一的3位课程ID
        self.name = name  # 课程名称
        self.mark = random.randint(25, 100)  # 随机生成成绩（25-100）
        self.grade = self.calculate_grade()  # 根据成绩计算等级

    def generate_id(self):
        # 确保生成的ID唯一
        while True:
            new_id = f"{random.randint(1, 999):03d}"  # 生成3位随机ID
            if new_id not in Subject.used_ids:  # 检查是否已存在
                Subject.used_ids.add(new_id)  # 添加到已使用ID集合
                return new_id

    def calculate_grade(self):
        # 根据成绩计算等级
        if self.mark >= 85:
            return "HD"  # High Distinction
        elif self.mark >= 75:
            return "D"  # Distinction
        elif self.mark >= 65:
            return "C"  # Credit
        elif self.mark >= 50:
            return "P"  # Pass
        else:
            return "F"  # Fail
