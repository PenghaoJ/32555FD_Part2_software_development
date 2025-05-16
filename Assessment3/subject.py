import random

class Subject:
    def __init__(self, name):
        self.id = self.generate_id()
        self.name = name
        self.mark = random.randint(25, 100)
        self.grade = self.calculate_grade()

    def generate_id(self):
        return f"{random.randint(1, 999):03d}"

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

if __name__ == "__main__":
    subject_list = [
        "Programming Fundamentals",
        "Data Structures",
        "Algorithms",
        "Software Engineering"
    ]

    for name in subject_list:
        s = Subject(name)
        print(f"Subject: {s.name}, ID: {s.id}, Mark: {s.mark}, Grade: {s.grade}")
