from psycopg2 import DatabaseError
from connection import create_connection

# Function for creation sql tables 
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except DatabaseError as err:
        print(err)


if __name__ == '__main__':
    # table for groups
    sql_create_groups = """DROP TABLE IF EXISTS groups CASCADE;
    CREATE TABLE groups(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
    );"""
    #table for students
    sql_create_students = """DROP TABLE IF EXISTS students CASCADE;
    CREATE TABLE students(
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(150) NOT NULL,
    group_id INTEGER REFERENCES groups(id) 
    on delete cascade
    );"""
    #table for teachers
    sql_create_teachers = """DROP TABLE IF EXISTS teachers CASCADE;
    CREATE TABLE teachers(
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(150) NOT NULL
    );"""
    #table for subjects
    sql_create_subjects = """DROP TABLE IF EXISTS subjects CASCADE;
    CREATE TABLE subjects(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    teacher_id INTEGER REFERENCES teachers(id)
    on delete cascade
    );"""
    #table for marks
    sql_create_marks_with_time = """DROP TABLE IF EXISTS marks CASCADE;
    CREATE TABLE marks(
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id)
    on delete cascade,
    subject_id INTEGER REFERENCES subjects(id)
    on delete cascade,
    grade INTEGER CHECK (grade >= 0 AND grade <= 100),
    grade_date DATE NOT NULL
    );"""

    
    with create_connection() as conn:
        if conn is not None:
            create_table(conn, sql_create_groups)
            create_table(conn, sql_create_students)
            create_table(conn, sql_create_teachers)
            create_table(conn, sql_create_subjects)
            create_table(conn, sql_create_marks_with_time)
        else:
            print("Error: can't create the database connection")