import sqlite3

conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    writer TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

conn.commit()
conn.close()
print("✅ Database initialized successfully!")
