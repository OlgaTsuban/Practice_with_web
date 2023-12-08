from random import randint, choice
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
from conf.db import session
from conf.models import Teacher, Student, Group, Subject, Mark

fake = Faker()

# Constants for presenting amount of students, groups, subjects, teachers and students for each group
AMOUNT_STUDENTS = randint(30, 50)
AMOUNT_GROUPS = 3
AMOUNT_SUBJECTS = randint(5, 8)
AMOUNT_TEACHERS = randint(3, 5)
MAX_AMOUNT_MARKS = 20
AMOUNT_STUDENTS_PER_GROUP = int(AMOUNT_STUDENTS/AMOUNT_GROUPS)

# Insert groups table using Faker()
def insert_groups():
    for _ in range(AMOUNT_GROUPS):
        group = Group(
            name=fake.word()
        )
        session.add(group)

# Insert teachers table using Faker()
def insert_teachers():
    for _ in range(AMOUNT_TEACHERS):
        teacher = Teacher(
            fullname=fake.name(),
        )
        session.add(teacher)

# Insert students table using Faker()
def insert_students():
    for _ in range(AMOUNT_STUDENTS):
        student = Student(
                fullname=fake.name(),
                group_id=choice(session.query(Group.id).all())[0],
            )
        session.add(student)

# Insert subjects table using Faker()
def insert_subjects():
    for _ in range(AMOUNT_SUBJECTS):
        subject = Subject(
                name=fake.word(),
                teacher_id=choice(session.query(Teacher.id).all())[0],
            )
        session.add(subject)

# Insert marks table using Faker() - is helping function
def insert_marks(student_id, subject_id):
    mark = Mark(
        grade = randint(1, 100),
        grade_date = fake.date_between(start_date='-30d', end_date='today'),
        student_id = student_id,
        subject_id = subject_id,
    )
    session.add(mark)

# Insert mark table - main function for marks 
def full_marks(students, subjects):
    for student in students:
        for subject in subjects:
            insert_marks(student.id, subject.id)

if __name__ == '__main__':
    try:
        # Insert groups, students, teachers, subjects
        insert_groups()
        insert_students()
        insert_teachers()
        insert_subjects()
        session.commit()

        # Insert marks for each student and subject
        students = session.query(Student).all()
        subjects = session.query(Subject).all()
        full_marks(students, subjects)
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()