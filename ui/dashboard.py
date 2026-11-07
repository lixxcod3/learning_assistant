import streamlit as st
import os
from database.db import get_user_profile
from gamification.levels import calculate_level_stats
from gamification.badges import get_all_badges_status

def render_dashboard_page():
    st.title("👤 My Profile & Files")
    
    # --- Profile Stats ---
    profile = get_user_profile()
    stats = calculate_level_stats(profile['xp'])
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Current Level", f"Level {stats['current_level']}")
    with col2: st.metric("Total XP", profile['xp'])
    with col3: st.metric("Highest Streak", profile['current_streak'])
        
    st.divider()
    
    # --- File Browser ---
    st.subheader("📂 Saved Lecture Folders")
    lectures_dir = os.path.join("data", "lectures")
    
    if os.path.exists(lectures_dir) and os.listdir(lectures_dir):
        for folder in os.listdir(lectures_dir):
            with st.expander(f"📁 {folder}"):
                folder_path = os.path.join(lectures_dir, folder)
                
                # List all files inside the folder
                files = os.listdir(folder_path)
                if not files:
                    st.write("Folder is empty.")
                    continue
                    
                for file_name in files:
                    file_path = os.path.join(folder_path, file_name)
                    # Provide a download button for each file
                    with open(file_path, "rb") as f:
                        file_bytes = f.read()
                        st.download_button(
                            label=f"⬇️ Download {file_name}",
                            data=file_bytes,
                            file_name=file_name,
                            key=file_path
                        )
    else:
        st.info("You haven't saved any lectures yet.")

    st.divider()

    # --- Badges ---
    st.subheader("🎖️ Achievement Badges")
    badges = get_all_badges_status()
    b_col1, b_col2 = st.columns(2)
    for idx, badge in enumerate(badges):
        col = b_col1 if idx % 2 == 0 else b_col2
        with col:
            if badge['unlocked']:
                st.success(f"**🏅 {badge['name']}**\n\n*{badge['description']}*")
            else:
                st.markdown(f"<div style='opacity: 0.5; border: 1px dashed gray; padding: 10px; border-radius: 5px; margin-bottom: 10px;'><strong>🔒 {badge['name']}</strong><br><em>{badge['description']}</em></div>", unsafe_allow_html=True)