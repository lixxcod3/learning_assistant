from database.db import get_user_profile, get_unlocked_badges, unlock_badge

# Badge Definitions matching your project spec
BADGES = {
    "First Step": "Complete your first quiz.",
    "Quick Learner": "Get 5 correct answers in a row.",
    "Perfect Mind": "Achieve 100% on a quiz.",
    "Consistent Learner": "Complete 3 quizzes."
}

def check_and_award_badges(perfect_score=False):
    """
    Evaluates current user stats and awards any newly earned badges.
    Returns a list of newly unlocked badge names to notify the user in the UI.
    """
    profile = get_user_profile()
    unlocked_badges = get_unlocked_badges()
    newly_unlocked = []

    def award(badge_name):
        if badge_name not in unlocked_badges:
            unlock_badge(badge_name)
            newly_unlocked.append(badge_name)

    # Check "First Step" (Complete your first quiz)
    if profile["quizzes_completed"] >= 1:
        award("First Step")

    # Check "Consistent Learner" (Complete 3 quizzes)
    if profile["quizzes_completed"] >= 3:
        award("Consistent Learner")

    # Check "Quick Learner" (Get 5 correct answers in a row)
    if profile["current_streak"] >= 5:
        award("Quick Learner")

    # Check "Perfect Mind" (Achieve 100%)
    # This boolean is passed from the quiz completion logic
    if perfect_score:
        award("Perfect Mind")

    return newly_unlocked

def get_all_badges_status():
    """
    Returns a dictionary of all badges and their locked/unlocked status 
    for displaying on the dashboard.
    """
    unlocked_badges = get_unlocked_badges()
    status_list = []
    
    for name, description in BADGES.items():
        status_list.append({
            "name": name,
            "description": description,
            "unlocked": name in unlocked_badges
        })
        
    return status_list