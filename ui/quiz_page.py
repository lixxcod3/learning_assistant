import streamlit as st
import os, json
from database.db import update_lecture_materials

def render_quiz_page():
    st.title("🎮 Knowledge Quiz")
    
    if 'last_feedback' not in st.session_state:
        st.session_state['last_feedback'] = None
    if 'q_idx' not in st.session_state:
        st.session_state['q_idx'] = 0
    if 'q_correct' not in st.session_state:
        st.session_state['q_correct'] = 0
    if 'q_done' not in st.session_state:
        st.session_state['q_done'] = False
    if 'q_saved' not in st.session_state:
        st.session_state['q_saved'] = False
    
    lecture_id = st.session_state.get('active_lecture_id')
    if not lecture_id:
        st.warning("Please open a lecture on the Upload page first.")
        return

    quiz_data = st.session_state.get('temp_quiz', [])
    if not quiz_data:
        st.info("No active quiz. Go to the Summary page to generate one.")
        return

    if 'q_idx' not in st.session_state:
        st.session_state['q_idx'] = 0
        st.session_state['q_correct'] = 0
        st.session_state['q_done'] = False
        st.session_state['last_feedback'] = None
        st.session_state['q_saved'] = False
        st.session_state['q_warning'] = None

    # --- END OF QUIZ LOGIC ---
    if st.session_state['q_done']:
        pct = (st.session_state['q_correct'] / len(quiz_data)) * 100
        if pct >= 60:
            st.success(f"🎉 You passed the test! Score: {pct:.0f}%")
            st.balloons()
        else:
            st.error(f"Keep practicing! Score: {pct:.0f}%")
            
        st.divider()

        # Save Warning Logic
        if not st.session_state.get('q_saved'):
            st.warning("⚠️ This quiz hasn't been saved yet.")
            
            # --- Align all buttons in one horizontal line ---
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💾 Save Quiz"):
                    # Save to DB
                    update_lecture_materials(lecture_id, quizzes=quiz_data)
                    
                    # Ensure the folder exists before saving to prevent FileNotFoundError
                    lec_title = st.session_state.get('active_lecture_title', 'unknown')
                    folder_dir = os.path.join("data", "lectures", lec_title)
                    os.makedirs(folder_dir, exist_ok=True)
                    
                    # Save to Folder
                    q_path = os.path.join(folder_dir, "quiz.json")
                    with open(q_path, "w") as f:
                        json.dump(quiz_data, f, indent=4)
                        
                    st.session_state['q_saved'] = True
                    st.session_state['q_warning'] = None
                    st.rerun()

            with col2:
                if st.button("🔄 Retake (Without Saving)"): 
                    st.session_state['q_warning'] = 'retake'
                    
            with col3:
                if st.button("✨ Generate New (Discard Current)"): 
                    st.session_state['q_warning'] = 'new'
                
            # Confirmation Prompt
            if st.session_state.get('q_warning'):
                st.error("Are you sure you want to discard this quiz? It will be lost.")
                if st.button("Yes, I'm sure"):
                    if st.session_state['q_warning'] == 'retake':
                        st.session_state['q_idx'] = 0
                        st.session_state['q_correct'] = 0
                        st.session_state['q_done'] = False
                        st.session_state['q_warning'] = None
                        st.rerun()
                    else:
                        st.session_state['temp_quiz'] = []
                        st.info("Discarded. Go to the Summary page to generate a new quiz.")
        else:
            st.success("✅ Quiz is saved in your lecture folder.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Retake"):
                    st.session_state['q_idx'] = 0
                    st.session_state['q_correct'] = 0
                    st.session_state['q_done'] = False
                    st.rerun()
            with col2:
                if st.button("✨ Generate New (Clear Current)"):
                    st.session_state['temp_quiz'] = []
                    st.session_state['q_saved'] = False
                    st.session_state['q_done'] = False
                    st.rerun()
        return

    # --- ACTIVE QUIZ LOGIC ---
    idx = st.session_state['q_idx']
    q = quiz_data[idx]
    
    st.markdown(f"### Question {idx + 1} of {len(quiz_data)}")
    st.write(f"**{q['question']}**")
    selected_option = st.radio("Select your answer:", q['options'], key=f"radio_{idx}")
    
    if st.session_state['last_feedback']:
        feedback = st.session_state['last_feedback']
        if feedback['correct']: st.success(feedback['msg'])
        else: st.error(feedback['msg'])
        st.info(f"**Explanation:** {feedback['exp']}")
        
        if st.button("Next Question"):
            st.session_state['last_feedback'] = None
            st.session_state['q_idx'] += 1
            if st.session_state['q_idx'] >= len(quiz_data):
                st.session_state['q_done'] = True
            st.rerun()
    else:
        if st.button("Submit Answer"):
            is_correct = (selected_option == q['answer'])
            if is_correct: st.session_state['q_correct'] += 1
            st.session_state['last_feedback'] = {
                'correct': is_correct,
                'msg': "Correct!" if is_correct else "Incorrect.",
                'exp': q.get('explanation', '')
            }
            st.rerun()