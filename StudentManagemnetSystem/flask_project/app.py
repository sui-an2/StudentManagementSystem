from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# 首页 - 重定向到 login
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

# 注册
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

# 登录
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))
        else:
            return "Login failed. <a href='/login'>Try again</a>"

    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

# 学生列表
@app.route("/students")
def students():
    if "username" not in session:
        return redirect(url_for("login"))
    
    search = request.args.get("search", "")
    
    conn = get_db_connection()
    if search:
        students = conn.execute(
            "SELECT * FROM students WHERE name LIKE ? OR student_id LIKE ?",
            (f"%{search}%", f"%{search}%")
        ).fetchall()
    else:
        students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template("students.html", students=students, search=search)

# 新增学生
@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        student_id = request.form["student_id"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        semester = request.form["semester"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO students (student_id, name, email, phone, course, semester) VALUES (?, ?, ?, ?, ?, ?)",
            (student_id, name, email, phone, course, semester)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    return render_template("add_student.html")

# 修改学生
@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        student_id = request.form["student_id"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        semester = request.form["semester"]

        conn.execute(
            "UPDATE students SET student_id=?, name=?, email=?, phone=?, course=?, semester=? WHERE id=?",
            (student_id, name, email, phone, course, semester, id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    student = conn.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()
    conn.close()

    return render_template("edit_student.html", student=student)

# 删除学生
@app.route("/delete_student/<int:id>")
def delete_student(id):
    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("students"))

# 报告
@app.route("/report")
def report():
    if "username" not in session:
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    report_data = conn.execute(
        "SELECT course, COUNT(*) as count FROM students GROUP BY course"
    ).fetchall()
    conn.close()

    return render_template("report.html", report_data=report_data)

# 登出
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)