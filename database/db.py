import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'progress.db')

def get_connection():
    """Establish and return a database connection."""
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize the database tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # User profile table for XP and Streaks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY DEFAULT 1,
            xp INTEGER DEFAULT 0,
            current_streak INTEGER DEFAULT 0,
            quizzes_completed INTEGER DEFAULT 0
        )
    ''')

    # Badges table to track unlocked achievements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            badge_name TEXT UNIQUE,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Insert default user row if it doesn't exist
    cursor.execute('SELECT COUNT(*) FROM user_profile')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO user_profile (id, xp, current_streak, quizzes_completed) VALUES (1, 0, 0, 0)')

    conn.commit()
    conn.close()

def get_user_profile():
    """Fetch the current user profile stats."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT xp, current_streak, quizzes_completed FROM user_profile WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"xp": row[0], "current_streak": row[1], "quizzes_completed": row[2]}
    return {"xp": 0, "current_streak": 0, "quizzes_completed": 0}

def update_user_stats(xp_added, correct_streak_added, completed_quiz=False):
    """Update XP and streak. Adds 1 to quizzes_completed if completed_quiz is True."""
    conn = get_connection()
    cursor = conn.cursor()
    
    quiz_increment = 1 if completed_quiz else 0
    
    cursor.execute('''
        UPDATE user_profile 
        SET xp = xp + ?, 
            current_streak = current_streak + ?,
            quizzes_completed = quizzes_completed + ?
        WHERE id = 1
    ''', (xp_added, correct_streak_added, quiz_increment))
    
    conn.commit()
    conn.close()

def unlock_badge(badge_name):
    """Save a new unlocked badge."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO badges (badge_name) VALUES (?)', (badge_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        # Badge already unlocked
        pass
    finally:
        conn.close()

def get_unlocked_badges():
    """Return a list of unlocked badge names."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT badge_name FROM badges')
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]