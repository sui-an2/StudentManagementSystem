import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    ("admin", "1234")
)

conn.commit()
conn.close()

print("User inserted")
