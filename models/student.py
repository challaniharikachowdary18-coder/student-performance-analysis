from db import fetch_all, fetch_one, execute

class Student:
    @staticmethod
    def all():
        return fetch_all("SELECT * FROM students ORDER BY roll_no")

    @staticmethod
    def get(student_id):
        return fetch_one("SELECT * FROM students WHERE student_id=%s", (student_id,))

    @staticmethod
    def create(roll_no, name, section):
        if not roll_no or not name or not section:
            raise ValueError("All student fields are required.")
        return execute("INSERT INTO students (roll_no,name,section) VALUES (%s,%s,%s)",
                       (roll_no, name, section))

    @staticmethod
    def update(student_id, roll_no, name, section):
        if not roll_no or not name or not section:
            raise ValueError("All student fields are required.")
        execute("UPDATE students SET roll_no=%s,name=%s,section=%s WHERE student_id=%s",
                (roll_no, name, section, student_id))

    @staticmethod
    def delete(student_id):
        execute("DELETE FROM students WHERE student_id=%s", (student_id,))
