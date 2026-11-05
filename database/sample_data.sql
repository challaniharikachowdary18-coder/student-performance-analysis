USE student_performance;
INSERT IGNORE INTO students (roll_no,name,section) VALUES
('23AIML001','Aarav Sharma','A'),
('23AIML002','Diya Reddy','A'),
('23AIML003','Kabir Rao','B'),
('23AIML004','Meera Das','B');

INSERT IGNORE INTO subjects (subject_name,max_marks,pass_marks) VALUES
('Python',100,35),('Mathematics',100,35),('Database Systems',100,35);

INSERT INTO marks (student_id,subject_id,assessment,marks_obtained)
SELECT s.student_id, sub.subject_id, 'Midterm', v.score
FROM (
 SELECT '23AIML001' roll_no,'Python' subject_name,91 score UNION ALL
 SELECT '23AIML001','Mathematics',84 UNION ALL
 SELECT '23AIML001','Database Systems',88 UNION ALL
 SELECT '23AIML002','Python',76 UNION ALL
 SELECT '23AIML002','Mathematics',68 UNION ALL
 SELECT '23AIML002','Database Systems',81 UNION ALL
 SELECT '23AIML003','Python',42 UNION ALL
 SELECT '23AIML003','Mathematics',31 UNION ALL
 SELECT '23AIML003','Database Systems',55 UNION ALL
 SELECT '23AIML004','Python',63 UNION ALL
 SELECT '23AIML004','Mathematics',72 UNION ALL
 SELECT '23AIML004','Database Systems',69
) v
JOIN students s ON s.roll_no=v.roll_no
JOIN subjects sub ON sub.subject_name=v.subject_name
WHERE NOT EXISTS (
 SELECT 1 FROM marks m
 WHERE m.student_id=s.student_id AND m.subject_id=sub.subject_id AND m.assessment='Midterm'
);
