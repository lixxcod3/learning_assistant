import streamlit as st
from database.db import get_user_profile, get_unlocked_badges, unlock_badge

BADGES = {
    "First Step": "Complete your first quiz.",
    "Quick Learner": "Get 5 correct answers in a row.",
    "Perfect Mind": "Achieve 100% on a quiz.",
    "Consistent Learner": "Complete 3 quizzes."
}

def check_and_award_badges(perfect_score=False):
    if 'user_id' not in st.session_state:
        return []
        
    user_id = st.session_state['user_id']
    profile = get_user_profile(user_id)
    unlocked_badges = get_unlocked_badges(user_id)
    newly_unlocked = []

    def award(badge_name):
        if badge_name not in unlocked_badges:
            unlock_badge(user_id, badge_name)
            newly_unlocked.append(badge_name)

    if profile["quizzes_completed"] >= 1:
        award("First Step")
    if profile["quizzes_completed"] >= 3:
        award("Consistent Learner")
    if profile["current_streak"] >= 5:
        award("Quick Learner")
    if perfect_score:
        award("Perfect Mind")

    return newly_unlocked

def get_all_badges_status(user_id):
    unlocked_badges = get_unlocked_badges(user_id)
    status_list = []
    
    for name, description in BADGES.items():
        status_list.append({
            "name": name,
            "description": description,
            "unlocked": name in unlocked_badges
        })
        
    return status_list