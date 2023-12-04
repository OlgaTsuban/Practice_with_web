SELECT s.group_id, ROUND(AVG(g.grade), 2) AS average_grade
FROM students s
JOIN marks g ON s.id = g.student_id
WHERE g.subject_id = 1
GROUP BY s.group_id
ORDER BY average_grade DESC;