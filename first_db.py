import sqlite3
 
conn = sqlite3.connect("school.db")
cur = conn.cursor()
 
cur.execute("""CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, age INTEGER, major TEXT)""")
 
cur.execute(
    "INSERT INTO students (name, age, major) VALUES (?, ?, ?)",
    ("Ayu", 19, "Informatics"))
 
conn.commit()
conn.close()