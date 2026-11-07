import streamlit as st
from database.db import get_lecture_data
from ai.flashcards import generate_flashcards
from ai.quiz_generator import generate_quiz

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
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📇 Generate Flashcards")
        fc_count = st.selectbox("How many flashcards?", [5, 10, 15, 20])
        if st.button("Generate Flashcards"):
            with st.spinner("Generating concise flashcards..."):
                new_fc = generate_flashcards(data['transcript'], count=fc_count)
                # Save to temporary state instead of DB
                st.session_state['temp_flashcards'] = new_fc['flashcards']
                st.session_state['fc_saved'] = False
                # Reset flashcard test state
                st.session_state['fc_idx'] = 0 
                st.session_state['fc_flipped'] = False
                st.session_state['fc_correct'] = 0
            st.success("Flashcards ready! Go to the Flashcards tab to take the test.")

    with col2:
        st.subheader("🎮 Generate Quiz")
        q_count = st.selectbox("How many questions?", [5, 10, 15, 20])
        if st.button("Generate Quiz"):
            with st.spinner("Generating quiz questions..."):
                new_q = generate_quiz(data['transcript'], count=q_count)
                # Save to temporary state instead of DB
                st.session_state['temp_quiz'] = new_q['quiz']
                st.session_state['q_saved'] = False
                # Reset quiz test state
                st.session_state['q_idx'] = 0
                st.session_state['q_correct'] = 0
                st.session_state['q_done'] = False
            st.success("Quiz ready! Go to the Quiz tab to take the test.")