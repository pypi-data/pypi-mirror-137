class Person:
    def __init__(self, fname, sname, type):
        self.fname = fname
        self.sname = sname
        self.type = type
        self.email = f"{fname}.{sname}@school.com"
        
    def fullname(self):
        """
        Return full name of person
        """
        return f'{self.fname} {self.sname}'

class Student(Person):
    def __init__(self, fname, sname, type, lesson_count):
        super().__init__(fname, sname, type)
        self.lesson_count = lesson_count
        
class Teacher(Person):
    def __init__(self, fname, sname, type, hourly_rate, students=None):
        super().__init__(fname, sname, type)
        self.hourly_rate = hourly_rate
        
        if students is None:
            self.students = []
        else:
            self.students = students
            
    def add_student(self, students):
        """
        student -- arry of students
        Add students to a teacher
        """
        for student in students:
            self.students.append(student)
            
    def remove_student(self, students):
        """
        student -- array of students
        Remove students to a teacher
        """
        for student in students:
            if student in self.students:
                self.students.remove(student)
            
    def get_amount_owed(self):
        running_total = 0
        for student in self.students:
            running_total += student.lesson_count * self.hourly_rate
        return f"Total amount owed to Mr {self.fullname()} is: £{running_total}"  
            
    def print_students(self):
        print(f'Mr {self.fullname()} has the following students:')
        for student in self.students:
            print(f'{student.fullname()}')