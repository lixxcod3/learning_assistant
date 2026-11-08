import streamlit as st
from database.db import get_lecture_data
from ai.flashcards import generate_flashcards
from ai.quiz_generator import generate_quiz

def start_generation(task_name):
    """Callback to lock the UI by setting the generating state."""
    st.session_state['generating_task'] = task_name

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
    
    # Initialize the generating state if it doesn't exist
    if 'generating_task' not in st.session_state:
        st.session_state['generating_task'] = None
        
    # Boolean flag to disable UI elements
    is_generating = st.session_state['generating_task'] is not None

    col1, col2 = st.columns(2)
    
    # --- Flashcard Generation UI ---
    with col1:
        st.subheader("📇 Generate Flashcards")
        st.selectbox("How many flashcards?", [5, 10, 15, 20], key="fc_count", disabled=is_generating)
        
        st.button(
            "Generate Flashcards", 
            disabled=is_generating, 
            on_click=start_generation, 
            args=("flashcards",)
        )
        
        # Execute the flashcard generation if the state matches
        if st.session_state['generating_task'] == "flashcards":
            with st.spinner("Generating concise flashcards... please wait."):
                new_fc = generate_flashcards(data['transcript'], count=st.session_state['fc_count'])
                
                st.session_state['temp_flashcards'] = new_fc['flashcards']
                st.session_state['fc_idx'] = 0 
                st.session_state['fc_flipped'] = False
                st.session_state['fc_correct'] = 0
                st.session_state['fc_saved'] = False
                
                st.session_state['global_notification'] = {
                    'type': 'Flashcards',
                    'msg': f"Successfully generated {st.session_state['fc_count']} flashcards!"
                }
                
                st.session_state['generating_task'] = None
                st.rerun()

    # --- Quiz Generation UI ---
    with col2:
        st.subheader("🎮 Generate Quiz")
        st.selectbox("How many questions?", [5, 10, 15, 20], key="q_count", disabled=is_generating)
        
        st.button(
            "Generate Quiz", 
            disabled=is_generating, 
            on_click=start_generation, 
            args=("quiz",)
        )
        
        # Execute the quiz generation if the state matches
        if st.session_state['generating_task'] == "quiz":
            with st.spinner("Generating quiz questions... please wait."):
                new_q = generate_quiz(data['transcript'], count=st.session_state['q_count'])
                
                st.session_state['temp_quiz'] = new_q['quiz']
                st.session_state['q_idx'] = 0
                st.session_state['q_correct'] = 0
                st.session_state['q_done'] = False
                st.session_state['q_saved'] = False
                
                # Trigger global notification
                st.session_state['global_notification'] = {
                    'type': 'Quiz',
                    'msg': f"Successfully generated a {st.session_state['q_count']}-question quiz!"
                }
                
                st.session_state['generating_task'] = None
                st.rerun()