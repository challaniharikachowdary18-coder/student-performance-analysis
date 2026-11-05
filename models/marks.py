from db import fetch_all, execute

class Marks:
    @staticmethod
    def all():
        return fetch_all("""
            SELECT m.mark_id, s.name AS student_name, s.roll_no,
                   sub.subject_name, m.assessment, m.marks_obtained,
                   sub.max_marks, sub.pass_marks
            FROM marks m
            JOIN students s ON s.student_id=m.student_id
            JOIN subjects sub ON sub.subject_id=m.subject_id
            ORDER BY s.roll_no, sub.subject_name, m.assessment
        """)

    @staticmethod
    def create(student_id, subject_id, assessment, score):
        if not assessment:
            raise ValueError("Assessment name is required.")
        return execute("""
            INSERT INTO marks (student_id,subject_id,assessment,marks_obtained)
            VALUES (%s,%s,%s,%s)
        """, (student_id, subject_id, assessment, score))

    @staticmethod
    def update(mark_id, student_id, subject_id, assessment, score):
        if not assessment:
            raise ValueError("Assessment name is required.")
        execute("""
            UPDATE marks SET student_id=%s, subject_id=%s,
            assessment=%s, marks_obtained=%s WHERE mark_id=%s
        """, (student_id, subject_id, assessment, score, mark_id))

    @staticmethod
    def delete(mark_id):
        execute("DELETE FROM marks WHERE mark_id=%s", (mark_id,))
