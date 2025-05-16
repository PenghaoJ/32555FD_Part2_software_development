from subject import Subject
import random

class Student:
    def __init__(self, name, email, password):
        self.id =  self.generate_id()
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    def generate_id(self):
        return f"{random.randint(1, 999999):06d}"

    def enrol_subject(self, subject_name):
        if len(self.subjects) >= 4:
            return 'Cannot choose more than 4 subjects.'


        new_subject = Subject(subject_name)
        self.subjects.append(new_subject)
        return f'Enrolled in {subject_name} with mark {new_subject.mark}.'

if __name__ == "__main__":
        student = Student("Alice", "alice@university.com", "Password123")

        print(f"Student ID: {student.id}")
        print(f"Name: {student.name}")
        print(f"Email: {student.email}")
        print(f"Password: {student.password}")

        student.enrol_subject("Programming Fundamentals")
        student.enrol_subject("Data Structures")
        student.enrol_subject("AI")
        student.enrol_subject("Maths")

        print("--- Subject List ---")
        for subj in student.subjects:
            print(f"{subj.name} - Mark: {subj.mark}, Grade: {subj.grade}")