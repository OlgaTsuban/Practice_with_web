SELECT s.id, s.fullname, ROUND(AVG(m.grade), 2) AS average_grade
FROM teachers s
JOIN subjects subj ON subj.teacher_id = s.id
JOIN marks m ON s.id = m.subject_id
WHERE s.id = 1
GROUP BY s.id;