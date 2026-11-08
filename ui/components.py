import streamlit as st
import os
from database.db import get_lecture_data

def nav_to_lecture_tab(tab_name, lecture_id, lecture_title):
    """Callback to switch tabs, safely load data, and completely reset progress trackers."""
    st.session_state['active_lecture_id'] = lecture_id
    st.session_state['active_lecture_title'] = lecture_title
    st.session_state['nav_radio'] = tab_name
    
    # Safely fetch data
    data = get_lecture_data(lecture_id)
    st.session_state['temp_flashcards'] = data.get('flashcards', [])
    st.session_state['temp_quiz'] = data.get('quizzes', [])
    
    # FIX: Completely reset ALL Quiz trackers
    st.session_state['q_idx'] = 0
    st.session_state['q_correct'] = 0
    st.session_state['q_done'] = False
    st.session_state['q_saved'] = False
    st.session_state['last_feedback'] = None
    
    # FIX: Completely reset ALL Flashcard trackers
    st.session_state['fc_idx'] = 0
    st.session_state['fc_correct'] = 0
    st.session_state['fc_flipped'] = False
    st.session_state['fc_saved'] = False

def render_item_row(icon, label, tab_name, lec, item_type, prefix):
    """Renders an ultra-clean, flat text button."""
    st.button(f"{icon} {label}", key=f"{prefix}_btn_{item_type}_{lec['id']}", 
              use_container_width=True, on_click=nav_to_lecture_tab, 
              args=(tab_name, lec['id'], lec['title']))

def render_lecture_folder(lec, prefix="side"):
    """Renders the expandable folder."""
    with st.expander(f"📁 {lec['title']}"):
        folder_path = os.path.join("data", "lectures", lec['title'])
        
        # Playable Audio/Video
        if os.path.exists(folder_path):
            media_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.mp4', '.wav'))]
            if media_files:
                media_path = os.path.join(folder_path, media_files[0])
                if media_path.endswith('.mp4'):
                    st.video(media_path)
                else:
                    st.audio(media_path)
        
        # Clean File Links
        render_item_row("📝", "Lecture Summary", "Summary", lec, "summary", prefix)
        if lec.get('has_fc'):
            render_item_row("📇", "Flashcards", "Flashcards", lec, "flashcards", prefix)
        if lec.get('has_quiz'):
            render_item_row("🎮", "Knowledge Quiz", "Quiz", lec, "quiz", prefix)