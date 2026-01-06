import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Complaints table
cur.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    content TEXT,
    category TEXT,
    fraud_level TEXT
)
""")

# Police users table
cur.execute("""
CREATE TABLE IF NOT EXISTS police_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    police_name TEXT,
    police_id TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database initialized: complaints + police_users tables created")
