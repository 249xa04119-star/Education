import sqlite3

DB_NAME = "students.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS results (
        username TEXT,
        topic TEXT,
        accuracy REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def save_result(username, topic, accuracy):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO results (username, topic, accuracy) VALUES (?, ?, ?)",
        (username, topic, accuracy),
    )
    conn.commit()
    conn.close()

def get_all_results():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM results")
    data = c.fetchall()
    conn.close()
    return data
