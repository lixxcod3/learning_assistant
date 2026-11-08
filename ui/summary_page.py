import streamlit as st
from database.db import get_lecture_data
from ai.flashcards import generate_flashcards
from ai.quiz_generator import generate_quiz

def start_generation(task_name):
    st.session_state['generating_task'] = task_name

@st.dialog("✨ Generation Complete")
def success_dialog(task_name):
    st.write(f"Your new {task_name.lower()} have been successfully generated and merged with your saved collection!")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"🚀 Go to {task_name}", use_container_width=True):
            st.session_state['nav_radio'] = task_name
            st.session_state['show_success_dialog'] = None
            st.rerun()
    with c2:
        if st.button("❌ Close", use_container_width=True):
            st.session_state['show_success_dialog'] = None
            st.rerun()

def render_summary_page():
    st.title("📝 Lecture Summary & Generators")
    
    lecture_id = st.session_state.get('active_lecture_id')
    if not lecture_id:
        st.warning("No lecture selected. Go to the Upload page to create or open a lecture.")
        return

    data = get_lecture_data(lecture_id)
    
    st.header(f"Title: {data['title']}")
    st.info(data.get("summary", "No summary available."))
    
    st.header("🔑 Key Points")
    for point in data.get("key_points", []):
        st.markdown(f"- {point}")

    st.divider()
    
    if 'generating_task' not in st.session_state:
        st.session_state['generating_task'] = None
        
    is_generating = st.session_state['generating_task'] is not None

    col1, col2 = st.columns(2)
    
    # --- Flashcard Generation UI ---
    with col1:
        st.subheader("📇 Generate Flashcards")
        st.selectbox("How many flashcards?", [5, 10, 15, 20], key="fc_count", disabled=is_generating)
        
        st.button("Generate Flashcards", disabled=is_generating, on_click=start_generation, args=("flashcards",))
        
        if st.session_state['generating_task'] == "flashcards":
            with st.spinner("Generating concise flashcards... please wait."):
                new_fc = generate_flashcards(data['transcript'], count=st.session_state['fc_count'])
                
                # FIX: APPEND to existing flashcards instead of overwriting
                existing_fc = data.get('flashcards', [])
                st.session_state['temp_flashcards'] = existing_fc + new_fc['flashcards']
                
                st.session_state['fc_idx'] = 0 
                st.session_state['fc_flipped'] = False
                st.session_state['fc_correct'] = 0
                st.session_state['fc_saved'] = False
                
                st.session_state['show_success_dialog'] = "Flashcards"
                st.session_state['generating_task'] = None
                st.rerun()

    # --- Quiz Generation UI ---
    with col2:
        st.subheader("🎮 Generate Quiz")
        st.selectbox("How many questions?", [5, 10, 15, 20], key="q_count", disabled=is_generating)
        
        st.button("Generate Quiz", disabled=is_generating, on_click=start_generation, args=("quiz",))
        
        if st.session_state['generating_task'] == "quiz":
            with st.spinner("Generating quiz questions... please wait."):
                new_q = generate_quiz(data['transcript'], count=st.session_state['q_count'])
                
                # FIX: APPEND to existing quiz instead of overwriting
                existing_qz = data.get('quizzes', [])
                st.session_state['temp_quiz'] = existing_qz + new_q['quiz']
                
                st.session_state['q_idx'] = 0
                st.session_state['q_correct'] = 0
                st.session_state['q_done'] = False
                st.session_state['q_saved'] = False
                
                st.session_state['show_success_dialog'] = "Quiz"
                st.session_state['generating_task'] = None
                st.rerun()

    # Trigger Dialog Popup
    if st.session_state.get('show_success_dialog'):
        success_dialog(st.session_state['show_success_dialog'])