from connection import create_connection
 

if __name__ == '__main__':
    sql_query_one = """SELECT s.id, s.fullname, ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN marks g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;"""

    sql_query_two = """SELECT s.id, s.fullname, ROUND(AVG(g.grade), 2) AS average_grade
    FROM marks g
    JOIN students s ON s.id = g.student_id
    WHERE g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;"""

    sql_query_three = """SELECT s.group_id, ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN marks g ON s.id = g.student_id
    WHERE g.subject_id = 1
    GROUP BY s.group_id
    ORDER BY average_grade DESC;"""

    sql_query_four = """SELECT ROUND(AVG(grade), 2) AS average_grade
    FROM marks; """

    sql_query_five = """SELECT s.id, s.fullname, g.id
    FROM teachers s
    JOIN subjects g ON s.id = g.teacher_id
    WHERE g.teacher_id = 1;"""

    sql_query_six = """SELECT s.id, s.fullname
    FROM students s
    JOIN groups g ON s.group_id = g.id
    WHERE g.id = 1;"""

    sql_query_seven = """SELECT s.id AS student_id, s.fullname AS student_name, m.grade, m.grade_date
    FROM students s
    JOIN marks m ON s.id = m.student_id
    JOIN subjects subj ON m.subject_id = subj.id
    JOIN groups g ON s.group_id = g.id
    WHERE g.id = 1 AND subj.id = 2;"""

    sql_query_eight= """SELECT s.id, s.fullname, ROUND(AVG(m.grade), 2) AS average_grade
    FROM teachers s
    JOIN subjects subj ON subj.teacher_id = s.id
    JOIN marks m ON s.id = m.subject_id
    WHERE s.id = 1
    GROUP BY s.id;"""

    sql_query_nine= """SELECT DISTINCT s.id, s.fullname, subj.id , subj.name
    FROM students s
    JOIN marks m ON s.id = m.student_id
    JOIN subjects subj ON m.subject_id = subj.id
    WHERE s.id = 1;"""

    sql_query_ten= """SELECT DISTINCT s.id, s.fullname, subj.id , subj.name, t.id, t.fullname
    FROM students s
    JOIN marks m ON s.id = m.student_id
    JOIN subjects subj ON m.subject_id = subj.id
    JOIN teachers t ON subj.teacher_id = t.id
    WHERE s.id = 1 AND t.id = 1;"""

    sql_query_eleven = """SELECT s.id, s.fullname, t.id, t.fullname, ROUND(AVG(m.grade), 2) AS average_grade 
    FROM teachers t
    JOIN subjects subj ON t.id = subj.teacher_id
    JOIN marks m ON subj.id = m.subject_id
    JOIN students s ON m.student_id = s.id
    WHERE s.id = 1 AND t.id = 1
    GROUP BY s.id, t.id, s.fullname, t.fullname;"""

    sql_query_twelve = """SELECT s.id, s.fullname, MAX(m.grade_date) AS max_date
    FROM students s
    JOIN marks m ON s.id = m.student_id
    JOIN subjects subj ON m.subject_id = subj.id
    JOIN groups g ON s.group_id = g.id
    WHERE g.id = 1 AND subj.id = 1 
    GROUP BY s.id, s.fullname
    ORDER BY s.id, max_date DESC;"""

    
    with create_connection() as conn:
        if conn is not None:
            cur = conn.cursor()
            # Execute the query with the parameter
            cur.execute(sql_query_twelve)

            # Fetch all rows
            rows = cur.fetchall()

            # Print the results
            for row in rows:
                print(row)