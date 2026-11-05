from db import fetch_all, fetch_one, execute

class Subject:
    @staticmethod
    def all():
        return fetch_all("SELECT * FROM subjects ORDER BY subject_name")

    @staticmethod
    def get(subject_id):
        return fetch_one("SELECT * FROM subjects WHERE subject_id=%s", (subject_id,))

    @staticmethod
    def create(name, max_marks, pass_marks):
        if not name:
            raise ValueError("Subject name is required.")
        return execute(
            "INSERT INTO subjects (subject_name,max_marks,pass_marks) VALUES (%s,%s,%s)",
            (name, max_marks, pass_marks)
        )

    @staticmethod
    def delete(subject_id):
        execute("DELETE FROM subjects WHERE subject_id=%s", (subject_id,))
