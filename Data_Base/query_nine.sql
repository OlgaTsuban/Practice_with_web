SELECT DISTINCT s.id, s.fullname, subj.id , subj.name
FROM students s
JOIN marks m ON s.id = m.student_id
JOIN subjects subj ON m.subject_id = subj.id
WHERE s.id = 1;