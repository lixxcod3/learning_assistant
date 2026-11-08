import streamlit as st
from database.db import get_unlocked_badges, unlock_badge, increment_quiz_count, get_quiz_count

# Streamlined Badge Definitions
BADGES = {
    "First Step": "Complete your first quiz.",
    "Consistent Learner": "Complete 3 quizzes.",
    "Perfect Mind": "Achieve 100% on a quiz."
}

def check_and_award_badges(perfect_score=False):
    if 'user_id' not in st.session_state:
        return []
        
    user_id = st.session_state['user_id']
    
    # Increment the internal tracker used only for badges
    increment_quiz_count(user_id)
    quizzes_completed = get_quiz_count(user_id)
    
    unlocked_badges = get_unlocked_badges(user_id)
    newly_unlocked = []

    def award(badge_name):
        if badge_name not in unlocked_badges:
            unlock_badge(user_id, badge_name)
            newly_unlocked.append(badge_name)

    # Core Badge Logic
    if quizzes_completed >= 1:
        award("First Step")
    
    if quizzes_completed >= 3:
        award("Consistent Learner")
        
    if perfect_score:
        award("Perfect Mind")

    return newly_unlocked

def get_all_badges_status(user_id):
    """Returns a list mapping all available badges against the user's unlocked status."""
    unlocked_badges = get_unlocked_badges(user_id)
    status_list = []
    
    for name, description in BADGES.items():
        status_list.append({
            "name": name,
            "description": description,
            "unlocked": name in unlocked_badges
        })
        
    return status_list