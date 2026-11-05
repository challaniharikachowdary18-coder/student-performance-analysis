from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import Student, Subject, Marks
from services.performance import calculate_performance
from services.analytics import dashboard_stats, subject_summary, student_summary, detailed_performance, section_summary, chart_subject_averages, chart_pass_percentages
from utils.validators import parse_int, validate_marks

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def dashboard():
    stats = dashboard_stats()
    return render_template("dashboard.html", stats=stats)

@app.route("/students")
def students():
    return render_template("students.html", students=Student.all())

@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        try:
            Student.create(
                request.form["roll_no"].strip(),
                request.form["name"].strip(),
                request.form["section"].strip()
            )
            flash("Student added successfully.", "success")
            return redirect(url_for("students"))
        except Exception as exc:
            flash(f"Could not add student: {exc}", "danger")
    return render_template("add_student.html", student=None)

@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    student = Student.get(student_id)
    if not student:
        flash("Student not found.", "warning")
        return redirect(url_for("students"))
    if request.method == "POST":
        try:
            Student.update(student_id, request.form["roll_no"].strip(),
                           request.form["name"].strip(), request.form["section"].strip())
            flash("Student updated.", "success")
            return redirect(url_for("students"))
        except Exception as exc:
            flash(f"Could not update student: {exc}", "danger")
    return render_template("edit_student.html", student=student)

@app.post("/students/<int:student_id>/delete")
def delete_student(student_id):
    Student.delete(student_id)
    flash("Student deleted.", "success")
    return redirect(url_for("students"))

@app.route("/subjects")
def subjects():
    return render_template("subjects.html", subjects=Subject.all())

@app.post("/subjects/add")
def add_subject():
    try:
        max_marks = parse_int(request.form["max_marks"], "Maximum marks")
        pass_marks = parse_int(request.form["pass_marks"], "Passing marks")
        if max_marks <= 0 or not 0 <= pass_marks <= max_marks:
            raise ValueError("Passing marks must be between 0 and maximum marks.")
        Subject.create(request.form["subject_name"].strip(), max_marks, pass_marks)
        flash("Subject added.", "success")
    except Exception as exc:
        flash(f"Could not add subject: {exc}", "danger")
    return redirect(url_for("subjects"))

@app.post("/subjects/<int:subject_id>/delete")
def delete_subject(subject_id):
    Subject.delete(subject_id)
    flash("Subject deleted.", "success")
    return redirect(url_for("subjects"))

@app.route("/marks", methods=["GET", "POST"])
def marks():
    if request.method == "POST":
        try:
            student_id = parse_int(request.form["student_id"], "Student")
            subject_id = parse_int(request.form["subject_id"], "Subject")
            subject = Subject.get(subject_id)
            if not subject:
                raise ValueError("Select a valid subject.")
            score = float(request.form["marks_obtained"])
            validate_marks(score, subject["max_marks"])
            Marks.create(student_id, subject_id, request.form["assessment"].strip(), score)
            flash("Marks saved.", "success")
        except Exception as exc:
            flash(f"Could not save marks: {exc}", "danger")
        return redirect(url_for("marks"))
    return render_template("marks.html", marks=Marks.all(), students=Student.all(), subjects=Subject.all())

@app.route("/marks/<int:mark_id>/edit", methods=["GET", "POST"])
def edit_mark(mark_id):
    existing = next((m for m in Marks.all() if m["mark_id"] == mark_id), None)
    if not existing:
        flash("Mark record not found.", "warning")
        return redirect(url_for("marks"))
    if request.method == "POST":
        try:
            student_id = parse_int(request.form["student_id"], "Student")
            subject_id = parse_int(request.form["subject_id"], "Subject")
            subject = Subject.get(subject_id)
            if not subject:
                raise ValueError("Select a valid subject.")
            score = float(request.form["marks_obtained"])
            validate_marks(score, subject["max_marks"])
            Marks.update(mark_id, student_id, subject_id,
                         request.form["assessment"].strip(), score)
            flash("Marks updated.", "success")
            return redirect(url_for("marks"))
        except Exception as exc:
            flash(f"Could not update marks: {exc}", "danger")
    return render_template("edit_mark.html", mark=existing,
                           students=Student.all(), subjects=Subject.all())

@app.post("/marks/<int:mark_id>/delete")
def delete_mark(mark_id):
    Marks.delete(mark_id)
    flash("Mark record deleted.", "success")
    return redirect(url_for("marks"))

@app.route("/analytics")
def analytics():
    threshold = request.args.get("threshold", default=50, type=float)
    threshold = max(0, min(100, threshold))
    summaries = subject_summary()
    students_report = student_summary(threshold)
    chart_subject_averages()
    chart_pass_percentages()
    return render_template("analytics.html", summaries=summaries,
                           students_report=students_report, threshold=threshold)

@app.route("/reports")
def reports():
    return render_template("reports.html", students_report=student_summary(50),
                           summaries=subject_summary(), detailed=detailed_performance(), sections=section_summary())

@app.errorhandler(404)
def not_found(_):
    return render_template("base.html", page_error="Page not found."), 404

if __name__ == "__main__":
    app.run(debug=True)
