import streamlit as st
from gamification.scoring import process_answer, process_quiz_completion
from gamification.badges import check_and_award_badges

def render_quiz_page():
    st.title("🎮 Knowledge Quiz")
    
    if 'ai_materials' not in st.session_state:
        st.warning("No data found. Please go to the Upload page and process a file first.")
        return

    quiz_data = st.session_state['ai_materials'].get('quiz', [])
    
    if not quiz_data:
        st.info("No quiz generated for this lecture.")
        return

    # Initialize quiz state variables
    if 'q_idx' not in st.session_state:
        st.session_state['q_idx'] = 0
        st.session_state['q_correct'] = 0
        st.session_state['q_done'] = False
        st.session_state['recent_xp'] = 0
        st.session_state['new_badges'] = []
        st.session_state['last_feedback'] = None

    # --- Quiz Completed View ---
    if st.session_state['q_done']:
        st.success(f"Quiz Complete! You scored {st.session_state['q_correct']} out of {len(quiz_data)}.")
        st.balloons()
        
        st.write(f"**Total XP earned this quiz:** {st.session_state['recent_xp']} XP")
        
        if st.session_state['new_badges']:
            st.subheader("🏆 New Badges Unlocked!")
            for badge in st.session_state['new_badges']:
                st.write(f"- **{badge}**")
                
        if st.button("Restart Quiz"):
            # Clear state to start over
            del st.session_state['q_idx']
            st.rerun()
        return

    # --- Active Quiz View ---
    idx = st.session_state['q_idx']
    q = quiz_data[idx]
    
    st.markdown(f"### Question {idx + 1} of {len(quiz_data)}")
    st.write(f"**{q['question']}**")
    
    selected_option = st.radio("Select your answer:", q['options'], key=f"radio_{idx}")
    
    # If the user has submitted an answer, show feedback and the "Next" button
    if st.session_state['last_feedback']:
        feedback = st.session_state['last_feedback']
        if feedback['correct']:
            st.success(feedback['msg'])
        else:
            st.error(feedback['msg'])
            
        st.info(f"**Explanation:** {feedback['exp']}")
        
        if st.button("Next Question"):
            st.session_state['last_feedback'] = None
            st.session_state['q_idx'] += 1
            
            # Check if that was the last question
            if st.session_state['q_idx'] >= len(quiz_data):
                st.session_state['q_done'] = True
                
                # Process final quiz completion bonuses
                comp_res = process_quiz_completion(len(quiz_data), st.session_state['q_correct'])
                st.session_state['recent_xp'] += comp_res['bonus_xp_earned']
                
                # Check for any new badges
                perfect = (st.session_state['q_correct'] == len(quiz_data))
                badges = check_and_award_badges(perfect_score=perfect)
                st.session_state['new_badges'].extend(badges)
                
            st.rerun()
            
    # If waiting for user to submit
    else:
        if st.button("Submit Answer"):
            is_correct = (selected_option == q['answer'])
            
            # Call your gamification backend
            score_res = process_answer(is_correct)
            st.session_state['recent_xp'] += score_res['xp_earned']
            
            if is_correct:
                st.session_state['q_correct'] += 1
                msg = f"Correct! +{score_res['xp_earned']} XP. (Current Streak: {score_res['streak']})"
            else:
                msg = f"Incorrect. {score_res['status']}"
                
            # Store feedback to display on next render
            st.session_state['last_feedback'] = {
                'correct': is_correct,
                'msg': msg,
                'exp': q.get('explanation', 'No explanation provided.')
            }
            st.rerun()