from sqlalchemy import func, desc, select, and_
from conf.models import Mark, Teacher, Student, Group, Subject
from conf.db import session

# Here are examples of some sql query written on SQLAlchemy
# Here present all queries, obligation 1-10 and additional 11, 12

def sql_query_one():
    """SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;"""
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Mark.grade), 2).label('average_grade')) \
        .select_from(Student).join(Mark).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result 

def sql_query_two():
    """SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;"""
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Mark.grade), 2).label('average_grade')) \
        .select_from(Mark).join(Student).filter(Mark.subject_id == 1).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result 

def sql_query_three():
    """SELECT s.group_id, ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN marks g ON s.id = g.student_id
    WHERE g.subject_id = 1
    GROUP BY s.group_id
    ORDER BY average_grade DESC;""" 

    result = session.query(Student.group_id, func.round(func.avg(Mark.grade), 2).label('average_grade')) \
        .select_from(Student).join(Mark).filter(Mark.subject_id == 1).group_by(Student.group_id).order_by(
        desc('average_grade')).all()
    return result

def sql_query_four():
    """SELECT ROUND(AVG(grade), 2) AS average_grade
    FROM marks; """ 

    result = session.query(func.round(func.avg(Mark.grade), 2).label('average_grade')) \
        .select_from(Mark).all()
    return result

def sql_query_five():
    """SELECT s.id, s.fullname, g.id
    FROM teachers s
    JOIN subjects g ON s.id = g.teacher_id
    WHERE g.teacher_id = 1;"""

    result = session.query(Teacher.id, Teacher.fullname, Subject.id) \
        .select_from(Teacher).join(Subject, Teacher.id==Subject.teacher_id).filter(Subject.teacher_id == 1).all()
    return result
    
def sql_query_six():
    """SELECT s.id, s.fullname
    FROM students s
    JOIN groups g ON s.group_id = g.id
    WHERE g.id = 1;"""

    result = session.query(Student.id, Student.fullname) \
        .select_from(Student).join(Group).filter(Group.id == 1).all()
    return result 

def sql_query_seven():
    """SELECT s.id AS student_id, s.fullname AS student_name, m.grade, m.grade_date
    FROM students s
    JOIN marks m ON s.id = m.student_id
    JOIN subjects subj ON m.subject_id = subj.id
    JOIN groups g ON s.group_id = g.id
    WHERE g.id = 1 AND subj.id = 2;""" 

    result = session.query(Student.id.label('student_id'), Student.fullname.label('student_name'), Mark.grade, Mark.grade_date) \
    .select_from(Student) \
    .join(Mark, Student.id == Mark.student_id) \
    .join(Subject, Mark.subject_id == Subject.id) \
    .join(Group, Student.group_id == Group.id) \
    .filter(Group.id == 1, Subject.id == 2).all()
    return result

def sql_query_eight():
    """SELECT s.id, s.fullname, ROUND(AVG(m.grade), 2) AS average_grade
    FROM teachers s
    JOIN subjects subj ON subj.teacher_id = s.id
    JOIN marks m ON s.id = m.subject_id
    WHERE s.id = 1
    GROUP BY s.id;"""
    result = session.query(Teacher.id, Teacher.fullname, func.round(func.avg(Mark.grade), 2).label('average_grade')) \
    .select_from(Teacher) \
    .join(Subject, Subject.teacher_id == Teacher.id) \
    .join(Mark, Teacher.id == Mark.subject_id) \
    .filter(Teacher.id == 1).group_by(Teacher.id).all()
    return result

def sql_query_nine():
    """SELECT DISTINCT s.id, s.fullname, subj.id , subj.name
    FROM students s
    JOIN marks m ON s.id = m.student_id
    JOIN subjects subj ON m.subject_id = subj.id
    WHERE s.id = 1;""" 

    result = session.query(Student.id, Student.fullname, Subject.id, Subject.name) \
    .select_from(Student) \
    .join(Mark, Student.id == Mark.student_id) \
    .join(Subject, Mark.subject_id == Subject.id) \
    .filter(Student.id == 1).all()
    return result

def sql_query_ten():
    """SELECT DISTINCT s.id, s.fullname, subj.id , subj.name, t.id, t.fullname
    FROM students s
    JOIN marks m ON s.id = m.student_id
    JOIN subjects subj ON m.subject_id = subj.id
    JOIN teachers t ON subj.teacher_id = t.id
    WHERE s.id = 1 AND t.id = 1;""" 

    result = session.query(Student.id, Student.fullname, Subject.id, Subject.name, Teacher.id, Teacher.fullname) \
    .select_from(Student) \
    .join(Mark, Student.id == Mark.student_id) \
    .join(Subject, Mark.subject_id == Subject.id) \
    .join(Teacher, Subject.teacher_id == Teacher.id)\
    .filter(Student.id == 1, Teacher.id==1).all()
    return result

def sql_query_eleven():
    """SELECT s.id, s.fullname, t.id, t.fullname, ROUND(AVG(m.grade), 2) AS average_grade 
    FROM teachers t
    JOIN subjects subj ON t.id = subj.teacher_id
    JOIN marks m ON subj.id = m.subject_id
    JOIN students s ON m.student_id = s.id
    WHERE s.id = 1 AND t.id = 1
    GROUP BY s.id, t.id, s.fullname, t.fullname;"""

    result = session.query(Student.id, Student.fullname, Teacher.id, Teacher.fullname, func.round(func.avg(Mark.grade), 2).label('average_grade')) \
    .select_from(Teacher) \
    .join(Subject, Subject.teacher_id == Teacher.id) \
    .join(Mark, Subject.id == Mark.subject_id) \
    .join(Student, Mark.student_id == Student.id)\
    .filter(Student.id == 1, Teacher.id==1).group_by(Student.id, Student.fullname, Teacher.id, Teacher.fullname).all()
    return result

def sql_query_twelve():
    """SELECT max(grade_date)
    FROM marks g
    JOIN students s ON s.id = g.student_id
    WHERE g.subject_id = 1 AND s.group_id  = 1;

    SELECT s.id, s.fullname, g.grade, g.grade_date
    FROM marks g
    JOIN students s ON g.student_id = s.id
    WHERE g.subject_id = 1 AND s.group_id = 1 AND g.grade_date = (
        SELECT max(grade_date)
        FROM marks g
        JOIN students s ON s.id=g.student_id
        WHERE g.subject_id = 1 AND s.group_id = 1
    );"""

    subquery = (select(func.max(Mark.grade_date)).join(Student, Mark.student_id == Student.id).filter(and_(Mark.subject_id == 1, Student.group_id == 1))).scalar_subquery()
    result = session.query(Student.id.label('student_id'), Student.fullname.label('student_fullname'),
                           Mark.grade, Mark.grade_date) \
        .select_from(Mark)\
        .join(Student) \
        .filter(and_(Mark.subject_id == 1, Student.group_id == 1, Mark.grade_date == subquery)) \
        .all()
    return result


if __name__ == '__main__':
    print(sql_query_twelve())
    
    