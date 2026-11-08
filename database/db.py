import sqlite3
import os
import json
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'progress.db')

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False) # Important for background generation

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Authentication Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')

    # User Progress (Linked to user_id)
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profile (
        user_id INTEGER PRIMARY KEY, xp INTEGER DEFAULT 0, 
        current_streak INTEGER DEFAULT 0, quizzes_completed INTEGER DEFAULT 0)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS badges (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, badge_name TEXT, 
        unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(user_id, badge_name))''')
    
    # Lectures (Linked to user_id)
    cursor.execute('''CREATE TABLE IF NOT EXISTS lectures (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT,
        transcript TEXT, summary TEXT, key_points TEXT, flashcards TEXT, quizzes TEXT, UNIQUE(user_id, title))''')

    conn.commit()
    conn.close()

# --- Auth Functions ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
        user_id = cursor.lastrowid
        cursor.execute('INSERT INTO user_profile (user_id) VALUES (?)', (user_id,))
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def verify_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, hash_password(password)))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def check_user_exists(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    return bool(row)

# --- Updated Lecture & Profile Functions (Require user_id) ---
def save_lecture_initial(user_id, title, transcript, summary, key_points):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO lectures (user_id, title, transcript, summary, key_points, flashcards, quizzes) 
                          VALUES (?, ?, ?, ?, ?, '[]', '[]')''', 
                       (user_id, title, transcript, json.dumps(summary), json.dumps(key_points)))
        lecture_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        cursor.execute('''UPDATE lectures SET transcript=?, summary=?, key_points=? WHERE user_id=? AND title=?''',
                       (transcript, json.dumps(summary), json.dumps(key_points), user_id, title))
        cursor.execute('SELECT id FROM lectures WHERE user_id=? AND title=?', (user_id, title))
        lecture_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return lecture_id

def get_all_lectures(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM lectures WHERE user_id=? ORDER BY id DESC', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1]} for r in rows]

def get_lecture_data(lecture_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT title, transcript, summary, key_points, flashcards, quizzes FROM lectures WHERE id=?', (lecture_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "title": row[0], "transcript": row[1],
            "summary": json.loads(row[2]) if row[2] else {},
            "key_points": json.loads(row[3]) if row[3] else [],
            "flashcards": json.loads(row[4]) if row[4] else [],
            "quiz": json.loads(row[5]) if row[5] else []
        }
    return None

def update_lecture_materials(lecture_id, flashcards=None, quizzes=None):
    conn = get_connection()
    cursor = conn.cursor()
    if flashcards is not None:
        cursor.execute('SELECT flashcards FROM lectures WHERE id=?', (lecture_id,))
        existing = json.loads(cursor.fetchone()[0] or '[]')
        existing.extend(flashcards)
        cursor.execute('UPDATE lectures SET flashcards=? WHERE id=?', (json.dumps(existing), lecture_id))
    if quizzes is not None:
        cursor.execute('SELECT quizzes FROM lectures WHERE id=?', (lecture_id,))
        existing = json.loads(cursor.fetchone()[0] or '[]')
        existing.extend(quizzes)
        cursor.execute('UPDATE lectures SET quizzes=? WHERE id=?', (json.dumps(existing), lecture_id))
    conn.commit()
    conn.close()

def get_user_profile(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT xp, current_streak, quizzes_completed FROM user_profile WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return {"xp": row[0], "current_streak": row[1], "quizzes_completed": row[2]} if row else {"xp": 0, "current_streak": 0, "quizzes_completed": 0}

def update_user_stats(user_id, xp_added, correct_streak_added, completed_quiz=False):
    conn = get_connection()
    cursor = conn.cursor()
    quiz_inc = 1 if completed_quiz else 0
    cursor.execute('UPDATE user_profile SET xp = xp + ?, current_streak = current_streak + ?, quizzes_completed = quizzes_completed + ? WHERE user_id = ?', 
                   (xp_added, correct_streak_added, quiz_inc, user_id))
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