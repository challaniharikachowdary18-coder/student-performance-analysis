# Student Performance Analysis System

A beginner-friendly Flask + MySQL application to manage students, subjects and assessment marks, then analyze class performance with Pandas, NumPy and Matplotlib.

## Features
- Student CRUD (add, view, edit, delete)
- Subject setup with maximum and passing marks
- Assessment mark entry with range validation
- Dashboard KPIs
- Subject averages, median, minimum, maximum and pass percentages
- Student ranking and configurable at-risk threshold
- Matplotlib charts generated from saved MySQL data

## Grading rules
A subject result is **Pass** only when every recorded assessment is at or above that subject's `pass_marks`. The displayed student average is the mean percentage across their recorded assessment rows. Grades are A+ (90+), A (80–89.99), B (70–79.99), C (60–69.99), D (50–59.99), F (below 50). These rules are examples and can be adjusted to match institution policy.

## Requirements
- Python 3.10+
- MySQL Server 8+
- Git (for version control)

## Run locally (Windows PowerShell)
1. Install Python and MySQL Server. Start the MySQL service.
2. Open MySQL Workbench or the MySQL command line and run `database/schema.sql`.
3. Optional demo records: run `database/sample_data.sql`.
4. In a terminal, open this project folder:
   ```powershell
   cd student-performance-analysis
   ```
5. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again.
6. Install packages:
   ```powershell
   pip install -r requirements.txt
   ```
7. Copy `.env.example` to `.env`, then update `MYSQL_PASSWORD` and `SECRET_KEY`.
8. Start the app:
   ```powershell
   python app.py
   ```
9. Open http://127.0.0.1:5000

## Run tests
```powershell
python -m unittest discover -s tests -v
```

## GitHub
Create an empty GitHub repository named `student-performance-analysis`, then run:
```bash
git init
git add .
git commit -m "Initial commit: Student Performance Analysis System"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/student-performance-analysis.git
git push -u origin main
```
Never commit `.env`; `.gitignore` excludes it. Use `.env.example` as the safe template.

## Notes
- This is an educational starter application. Add authentication, role-based access, CSRF protection, audit logs and deployment configuration before using real student records.
- Use only sample or institution-approved data. Do not put real student personal information in a public repository.
