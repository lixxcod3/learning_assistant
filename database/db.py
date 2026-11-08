import sqlite3
import json
import os

DB_PATH = 'data/progress.db'

def get_connection():
    os.makedirs('data', exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            quizzes_completed INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS lectures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            transcript TEXT,
            summary TEXT,
            key_points TEXT,
            flashcards TEXT,
            quizzes TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS badges (
            user_id INTEGER,
            badge_name TEXT,
            UNIQUE(user_id, badge_name),
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    conn.commit()
    conn.close()

def check_user_exists(username):
    conn = get_connection()
    row = conn.cursor().execute('SELECT user_id FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return bool(row)

def create_user(username, password):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def verify_login(username, password):
    conn = get_connection()
    row = conn.cursor().execute('SELECT user_id FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    return row[0] if row else None

def save_lecture_initial(user_id, title, transcript, summary, key_points):
    conn = get_connection()
    cursor = conn.cursor()
    kp_json = json.dumps(key_points) if isinstance(key_points, list) else key_points
    cursor.execute('''
        INSERT INTO lectures (user_id, title, transcript, summary, key_points) 
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, title, transcript, summary, kp_json))
    conn.commit()
    lecture_id = cursor.lastrowid
    conn.close()
    return lecture_id

def get_all_lectures_full(user_id):
    conn = get_connection()
    rows = conn.cursor().execute(
        'SELECT id, title, flashcards, quizzes FROM lectures WHERE user_id = ? ORDER BY id DESC', 
        (user_id,)
    ).fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "has_fc": bool(r[2]), "has_quiz": bool(r[3])} for r in rows]

def get_lecture_data(lecture_id):
    conn = get_connection()
    row = conn.cursor().execute(
        'SELECT title, transcript, summary, key_points, flashcards, quizzes FROM lectures WHERE id = ?', 
        (lecture_id,)
    ).fetchone()
    conn.close()
    
    if row:
        return {
            "title": row[0], 
            "transcript": row[1], 
            "summary": row[2], 
            "key_points": json.loads(row[3]) if row[3] else [],
            "flashcards": json.loads(row[4]) if row[4] else [],
            "quizzes": json.loads(row[5]) if row[5] else []
        }
    return {}

def update_lecture_materials(lecture_id, flashcards=None, quizzes=None):
    conn = get_connection()
    cursor = conn.cursor()
    if flashcards is not None:
        cursor.execute('UPDATE lectures SET flashcards = ? WHERE id = ?', (json.dumps(flashcards), lecture_id))
    if quizzes is not None:
        cursor.execute('UPDATE lectures SET quizzes = ? WHERE id = ?', (json.dumps(quizzes), lecture_id))
    conn.commit()
    conn.close()

def unlock_badge(user_id, badge_name):
    conn = get_connection()
    try:
        conn.cursor().execute('INSERT INTO badges (user_id, badge_name) VALUES (?, ?)', (user_id, badge_name))
        conn.commit()
    except sqlite3.IntegrityError: 
        pass
    finally: 
        conn.close()

def get_unlocked_badges(user_id):
    conn = get_connection()
    rows = conn.cursor().execute('SELECT badge_name FROM badges WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return [row[0] for row in rows]

def increment_quiz_count(user_id):
    conn = get_connection()
    conn.cursor().execute('UPDATE users SET quizzes_completed = quizzes_completed + 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_quiz_count(user_id):
    conn = get_connection()
    row = conn.cursor().execute('SELECT quizzes_completed FROM users WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return row[0] if row else 0