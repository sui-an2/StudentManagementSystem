import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# users 表
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# students 表
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    course TEXT,
    semester TEXT
)
""")

conn.commit()
conn.close()

print("Database initialized with users and students tables")