from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from db import fetch_all

CHART_DIR = Path("static/charts")
CHART_DIR.mkdir(parents=True, exist_ok=True)

def marks_frame():
    rows = fetch_all("""
        SELECT s.student_id, s.roll_no, s.name, s.section,
               sub.subject_id, sub.subject_name, sub.max_marks, sub.pass_marks,
               m.assessment, m.marks_obtained
        FROM marks m
        JOIN students s ON s.student_id=m.student_id
        JOIN subjects sub ON sub.subject_id=m.subject_id
    """)
    return pd.DataFrame(rows)

def dashboard_stats():
    students = fetch_all("SELECT COUNT(*) AS n FROM students")[0]["n"]
    subjects = fetch_all("SELECT COUNT(*) AS n FROM subjects")[0]["n"]
    df = marks_frame()
    if df.empty:
        return {"students": students, "subjects": subjects, "average": 0, "pass_rate": 0}
    df["percentage"] = df["marks_obtained"] / df["max_marks"] * 100
    df["passed"] = df["marks_obtained"] >= df["pass_marks"]
    return {"students": students, "subjects": subjects,
            "average": round(float(np.mean(df["percentage"])), 2),
            "pass_rate": round(float(df["passed"].mean() * 100), 2)}

def subject_summary():
    df = marks_frame()
    if df.empty: return []
    df["percentage"] = df["marks_obtained"] / df["max_marks"] * 100
    df["passed"] = df["marks_obtained"] >= df["pass_marks"]
    result = df.groupby("subject_name").agg(
        average_percentage=("percentage", "mean"),
        median_percentage=("percentage", "median"),
        min_percentage=("percentage", "min"),
        max_percentage=("percentage", "max"),
        pass_percentage=("passed", lambda x: x.mean() * 100),
        assessment_count=("marks_obtained", "count")
    ).reset_index()
    return result.round(2).to_dict(orient="records")

def student_summary(threshold=50):
    df = marks_frame()
    if df.empty: return []
    df["percentage"] = df["marks_obtained"] / df["max_marks"] * 100
    result = df.groupby(["student_id", "roll_no", "name", "section"]).agg(
        average_percentage=("percentage", "mean"),
        total_assessments=("percentage", "count")
    ).reset_index()
    result["average_percentage"] = result["average_percentage"].round(2)
    result["status"] = np.where(result["average_percentage"] >= threshold, "On track", "Needs support")
    result = result.sort_values("average_percentage", ascending=False)
    return result.to_dict(orient="records")

def chart_subject_averages():
    data = subject_summary()
    if not data: return
    names = [x["subject_name"] for x in data]
    values = [x["average_percentage"] for x in data]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(names, values)
    ax.set(title="Subject-wise Average Percentage", ylabel="Average (%)", ylim=(0, 100))
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "subject_averages.png")
    plt.close(fig)

def chart_pass_percentages():
    data = subject_summary()
    if not data: return
    names = [x["subject_name"] for x in data]
    values = [x["pass_percentage"] for x in data]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(names, values)
    ax.set(title="Subject-wise Pass Percentage", ylabel="Pass (%)", ylim=(0, 100))
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "pass_percentages.png")
    plt.close(fig)


def detailed_performance():
    df = marks_frame()
    if df.empty:
        return []
    grouped = df.groupby(
        ["roll_no", "name", "section", "subject_name", "max_marks", "pass_marks"]
    ).agg(
        total=("marks_obtained", "sum"),
        assessment_count=("marks_obtained", "count"),
        average=("marks_obtained", "mean"),
        lowest=("marks_obtained", "min"),
        highest=("marks_obtained", "max"),
        failed_assessments=("marks_obtained", lambda values: int(
            (values < df.loc[values.index, "pass_marks"]).sum()
        ))
    ).reset_index()
    grouped["max_total"] = grouped["max_marks"] * grouped["assessment_count"]
    grouped["percentage"] = grouped["total"] / grouped["max_total"] * 100
    grouped["grade"] = pd.cut(
        grouped["percentage"],
        bins=[-0.001, 49.999, 59.999, 69.999, 79.999, 89.999, 100.001],
        labels=["F", "D", "C", "B", "A", "A+"]
    ).astype(str)
    grouped["status"] = np.where(grouped["failed_assessments"] == 0, "Pass", "Fail")
    numeric = ["total", "average", "percentage"]
    grouped[numeric] = grouped[numeric].round(2)
    return grouped.to_dict(orient="records")


def section_summary():
    """Summarize average marks and assessment pass rate by class section."""
    df = marks_frame()
    if df.empty:
        return []
    df["percentage"] = df["marks_obtained"] / df["max_marks"] * 100
    df["passed"] = df["marks_obtained"] >= df["pass_marks"]
    result = df.groupby("section").agg(
        student_count=("student_id", "nunique"),
        average_percentage=("percentage", "mean"),
        pass_percentage=("passed", lambda values: values.mean() * 100)
    ).reset_index()
    return result.round(2).to_dict(orient="records")
