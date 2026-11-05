def calculate_performance(scores, max_marks, pass_marks):
    """Calculate a student's result for one subject across recorded assessments."""
    if not scores:
        return {"total": 0, "max_total": 0, "average": 0.0,
                "percentage": 0.0, "grade": "N/A", "status": "No marks"}
    total = sum(float(x) for x in scores)
    max_total = max_marks * len(scores)
    percentage = (total / max_total) * 100 if max_total else 0
    average = total / len(scores)
    passed = all(float(x) >= pass_marks for x in scores)
    if percentage >= 90: grade = "A+"
    elif percentage >= 80: grade = "A"
    elif percentage >= 70: grade = "B"
    elif percentage >= 60: grade = "C"
    elif percentage >= 50: grade = "D"
    else: grade = "F"
    return {"total": round(total, 2), "max_total": max_total,
            "average": round(average, 2), "percentage": round(percentage, 2),
            "grade": grade, "status": "Pass" if passed else "Fail"}
