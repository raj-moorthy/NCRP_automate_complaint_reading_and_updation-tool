import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Add summary column if it doesn't exist
try:
    cur.execute("ALTER TABLE complaints ADD COLUMN summary TEXT")
    print("✅ 'summary' column added successfully")
except sqlite3.OperationalError as e:
    print("ℹ️ Column already exists or cannot be added:", e)

conn.commit()
conn.close()
