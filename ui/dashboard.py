import streamlit as st
from database.db import get_all_lectures_full
from ui.components import render_lecture_folder
from gamification.badges import get_all_badges_status

def render_dashboard_page():
    st.title("👤 My Profile & Files")
    
    if 'user_id' not in st.session_state:
        st.warning("You must sign in first.")
        return

    user_id = st.session_state['user_id']
    st.write(f"Welcome back, **{st.session_state.get('username', 'User')}**!")
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📂 All Lecture Folders")
        lectures = get_all_lectures_full(user_id)
        
        if lectures:
            with st.container(height=600):
                for lec in lectures:
                    render_lecture_folder(lec, prefix="dash")
        else:
            st.info("You haven't saved any lectures yet.")

    with col2:
        st.subheader("🎖️ Achievement Badges")
        try:
            badges = get_all_badges_status(user_id)
        except TypeError:
            badges = get_all_badges_status() 
            
        b_col1, b_col2 = st.columns(2)
        for idx, badge in enumerate(badges):
            col = b_col1 if idx % 2 == 0 else b_col2
            with col:
                if badge['unlocked']:
                    st.success(f"**🏅 {badge['name']}**\n\n*{badge['description']}*")
                else:
                    st.markdown(f"<div style='opacity: 0.5; border: 1px dashed gray; padding: 10px; border-radius: 5px; margin-bottom: 10px;'><strong>🔒 {badge['name']}</strong><br><em>{badge['description']}</em></div>", unsafe_allow_html=True)