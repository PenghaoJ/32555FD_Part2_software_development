from subject import Subject
import random

class Student:
    def __init__(self, name, email, password):
        self.id = self.generate_id()
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    def generate_id(self):
        number = random.randint(1, 999999)
        return f"{number:06d}"

    def enrol_subject(self, subject_name):
        if len(self.subjects) >= 4:
            return 'Cannot choose more than 4 subjects.'
        new_subject = Subject(subject_name)
        self.subjects.append(new_subject)
        return f'Enrolled in {subject_name} with mark {new_subject.mark}.'
        # Group C: Call this when student selects a subject

    def remove_subject_by_id(self, subject_id):
        self.subjects = [s for s in self.subjects if s.id != subject_id]
        # Group C: Call this when student removes a subject

    def get_average_mark(self):
        if not self.subjects:
            return 0
        total = sum(s.mark for s in self.subjects)
        return round(total / len(self.subjects), 2)
        # Group D: Use this in admin view to calculate student's average

    def get_pass_status(self):
        return "PASS" if self.get_average_mark() >= 50 else "FAIL"
        # Group D: Use this to determine pass/fail status

    def change_password(self, new_password):
        self.password = new_password
        # Group B: Call this when student changes password

    def get_subjects(self):
        return self.subjects
        # Use this to access enrolled subjects

    def get_id(self):
        return self.id
        # Group D: Used to identify student for admin removal
