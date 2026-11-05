from database.db import update_user_stats, get_user_profile

# Scoring Constants
XP_PER_CORRECT_ANSWER = 10
STREAK_BONUS_XP = 5
STREAK_THRESHOLD = 3      # Bonus every 3 correct answers in a row
QUIZ_COMPLETION_XP = 20
PERFECT_SCORE_XP = 50

def process_answer(is_correct):
    """
    Process a single quiz answer.
    Returns a dictionary detailing the XP earned and current streak.
    """
    profile = get_user_profile()
    current_streak = profile['current_streak']
    
    if is_correct:
        new_streak = current_streak + 1
        xp_earned = XP_PER_CORRECT_ANSWER
        
        # Award bonus XP if the user hits a streak threshold (e.g., 3, 6, 9 in a row)
        if new_streak % STREAK_THRESHOLD == 0:
            xp_earned += STREAK_BONUS_XP
            
        update_user_stats(xp_added=xp_earned, correct_streak_added=1, completed_quiz=False)
        return {"xp_earned": xp_earned, "streak": new_streak, "status": "Correct!"}
    
    else:
        # If wrong, XP is 0 and streak resets to 0. 
        # We subtract the current_streak to bring it to 0 in the DB.
        update_user_stats(xp_added=0, correct_streak_added=-current_streak, completed_quiz=False)
        return {"xp_earned": 0, "streak": 0, "status": "Incorrect. Streak reset."}

def process_quiz_completion(total_questions, correct_answers):
    """
    Process the end of a quiz, awarding completion and perfect score bonuses.
    """
    xp_earned = QUIZ_COMPLETION_XP
    
    # Check for perfect score
    if total_questions > 0 and correct_answers == total_questions:
        xp_earned += PERFECT_SCORE_XP
        
    update_user_stats(xp_added=xp_earned, correct_streak_added=0, completed_quiz=True)
    return {"bonus_xp_earned": xp_earned}