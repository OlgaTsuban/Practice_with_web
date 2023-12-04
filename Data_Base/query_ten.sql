SELECT DISTINCT s.id, s.fullname, subj.id , subj.name, t.id, t.fullname
FROM students s
JOIN marks m ON s.id = m.student_id
JOIN subjects subj ON m.subject_id = subj.id
JOIN teachers t ON subj.teacher_id = t.id
WHERE s.id = 1 AND t.id = 1;