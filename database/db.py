import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'progress.db')

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # User Progress Tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profile (
        id INTEGER PRIMARY KEY DEFAULT 1, xp INTEGER DEFAULT 0, 
        current_streak INTEGER DEFAULT 0, quizzes_completed INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS badges (
        id INTEGER PRIMARY KEY AUTOINCREMENT, badge_name TEXT UNIQUE, unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Lecture & Notes Management Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS lectures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        transcript TEXT,
        summary TEXT,
        key_points TEXT,
        flashcards TEXT,
        quizzes TEXT
    )''')

    cursor.execute('SELECT COUNT(*) FROM user_profile')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO user_profile (id, xp, current_streak, quizzes_completed) VALUES (1, 0, 0, 0)')

    conn.commit()
    conn.close()

# --- Lecture Management Functions ---
def save_lecture_initial(title, transcript, summary, key_points):
    """Saves the initial transcript and summary. Prevents overlapping by using unique titles."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO lectures (title, transcript, summary, key_points, flashcards, quizzes) 
                          VALUES (?, ?, ?, ?, '[]', '[]')''', 
                       (title, transcript, json.dumps(summary), json.dumps(key_points)))
        lecture_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # If title exists, update it instead of overlapping
        cursor.execute('''UPDATE lectures SET transcript=?, summary=?, key_points=? WHERE title=?''',
                       (transcript, json.dumps(summary), json.dumps(key_points), title))
        cursor.execute('SELECT id FROM lectures WHERE title=?', (title,))
        lecture_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return lecture_id

def get_all_lectures():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM lectures ORDER BY id DESC')
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
            "title": row[0],
            "transcript": row[1],
            "summary": json.loads(row[2]) if row[2] else {},
            "key_points": json.loads(row[3]) if row[3] else [],
            "flashcards": json.loads(row[4]) if row[4] else [],
            "quiz": json.loads(row[5]) if row[5] else []
        }
    return None

def update_lecture_materials(lecture_id, flashcards=None, quizzes=None):
    """Appends new flashcards or quizzes to the existing saved lecture."""
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

# --- Profile Functions (Keep these exactly as they were) ---
def get_user_profile():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT xp, current_streak, quizzes_completed FROM user_profile WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    return {"xp": row[0], "current_streak": row[1], "quizzes_completed": row[2]} if row else {"xp": 0, "current_streak": 0, "quizzes_completed": 0}

def update_user_stats(xp_added, correct_streak_added, completed_quiz=False):
    conn = get_connection()
    cursor = conn.cursor()
    quiz_increment = 1 if completed_quiz else 0
    cursor.execute('UPDATE user_profile SET xp = xp + ?, current_streak = current_streak + ?, quizzes_completed = quizzes_completed + ? WHERE id = 1', 
                   (xp_added, correct_streak_added, quiz_increment))
    conn.commit()
    conn.close()

def unlock_badge(badge_name):
    conn = get_connection()
    try:
        conn.cursor().execute('INSERT INTO badges (badge_name) VALUES (?)', (badge_name,))
        conn.commit()
    except sqlite3.IntegrityError: pass
    finally: conn.close()

def get_unlocked_badges():
    conn = get_connection()
    rows = conn.cursor().execute('SELECT badge_name FROM badges').fetchall()
    conn.close()
    return [row[0] for row in rows]