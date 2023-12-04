SELECT s.id, s.fullname, MAX(m.grade_date) AS max_date
FROM students s
JOIN marks m ON s.id = m.student_id
JOIN subjects subj ON m.subject_id = subj.id
JOIN groups g ON s.group_id = g.id
WHERE g.id = 1 AND subj.id = 1 
GROUP BY s.id, s.fullname
ORDER BY s.id, max_date DESC;