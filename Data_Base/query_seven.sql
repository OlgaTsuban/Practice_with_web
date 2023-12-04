SELECT s.id AS student_id, s.fullname AS student_name, m.grade, m.grade_date
FROM students s
JOIN marks m ON s.id = m.student_id
JOIN subjects subj ON m.subject_id = subj.id
JOIN groups g ON s.group_id = g.id
WHERE g.id = 1 AND subj.id = 2;