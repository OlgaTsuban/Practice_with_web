from faker import Faker
from random import randint
from connection import create_connection
from psycopg2 import DatabaseError


fake = Faker()

#Constants for presenting amount of students, groups, subjects, teachers and students for each group
AMOUNT_STUDENTS = randint(30, 50)
AMOUNT_GROUPS = 3
AMOUNT_SUBJECTS = randint(5, 8)
AMOUNT_TEACHERS = randint(3, 5)
AMOUNT_STUDENTS_PER_GROUP = int(AMOUNT_STUDENTS/AMOUNT_GROUPS)

if __name__ == '__main__':
    sql_insert_groups_table = """INSERT INTO groups (name) VALUES(%s)"""
    sql_insert_teachers_table = """INSERT INTO teachers (fullname) VALUES(%s)"""
    sql_insert_subjects_table = """INSERT INTO subjects (name, teacher_id) VALUES(%s, %s)"""
    sql_insert_students_table = """INSERT INTO students (fullname, group_id) VALUES(%s, %s) RETURNING id"""
    sql_insert_marks_table = """INSERT INTO marks (student_id, subject_id, grade, grade_date) VALUES(%s, %s, %s, %s)"""

    with create_connection() as conn:
        if conn is not None:
            cur = conn.cursor()

            #insert groups
            for _ in range(AMOUNT_GROUPS):
                cur.execute(sql_insert_groups_table, (fake.word(),))

            #insert teachers
            for _ in range(AMOUNT_TEACHERS):
                cur.execute(sql_insert_teachers_table, (fake.name(),))

            #insert subject
            for teacher_id in range(1, AMOUNT_TEACHERS):
                for _ in range(2):
                    cur.execute(sql_insert_subjects_table, (fake.word(), teacher_id))

            #insert student and marks
            for grout_id in range(1,AMOUNT_GROUPS+1):
                for _ in range(AMOUNT_STUDENTS_PER_GROUP):
                    cur.execute(sql_insert_students_table, (fake.name(), grout_id))
                    student_id = cur.fetchone()[0]
                    for subject_id in range(1, AMOUNT_SUBJECTS+1):
                        for _ in range(AMOUNT_GROUPS-1):
                            cur.execute(sql_insert_marks_table, (student_id, subject_id, randint(0, 100), fake.date_this_decade()))
        try:
            conn.commit()
        except DatabaseError as err:
            print(err)
            conn.rollback()