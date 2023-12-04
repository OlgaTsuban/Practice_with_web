SELECT s.id, s.fullname, t.id, t.fullname, ROUND(AVG(m.grade), 2) AS average_grade 
FROM teachers t
JOIN subjects subj ON t.id = subj.teacher_id
JOIN marks m ON subj.id = m.subject_id
JOIN students s ON m.student_id = s.id
WHERE s.id = 1 AND t.id = 1
GROUP BY s.id, t.id, s.fullname, t.fullname;