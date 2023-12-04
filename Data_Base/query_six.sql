SELECT s.id, s.fullname
FROM students s
JOIN groups g ON s.group_id = g.id
WHERE g.id = 1;