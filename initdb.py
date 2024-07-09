import sqlite3

def init_db():
    conn = sqlite3.connect('kanban.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 description TEXT,
                 status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()
