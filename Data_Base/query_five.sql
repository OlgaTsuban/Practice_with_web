SELECT s.id, s.fullname, g.id
FROM teachers s
JOIN subjects g ON s.id = g.teacher_id
WHERE g.teacher_id = 1;