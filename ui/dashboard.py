import streamlit as st
from database.db import get_user_profile
from gamification.levels import calculate_level_stats
from gamification.badges import get_all_badges_status

def render_dashboard_page():
    st.title("👤 My Profile & Dashboard")
    
    # Fetch live data from SQLite
    profile = get_user_profile()
    stats = calculate_level_stats(profile['xp'])
    
    # --- Top Section: Key Stats ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Level", f"Level {stats['current_level']}")
    with col2:
        st.metric("Total XP", profile['xp'])
    with col3:
        st.metric("Highest Streak", profile['current_streak'])
        
    st.divider()
    
    # --- Level Progress Bar ---
    st.subheader("Level Progress")
    if stats['next_level_xp'] == "MAX":
        st.progress(1.0)
        st.success("🎉 You have reached the maximum level!")
    else:
        st.write(f"XP to next level: **{stats['xp_into_level']} / {stats['xp_required']}**")
        st.progress(stats['progress_percent'] / 100.0)
        
    st.divider()
    
    # --- Achievements / Badges ---
    st.subheader("🎖️ Achievement Badges")
    badges = get_all_badges_status()
    
    # Display badges in a grid (2 columns)
    b_col1, b_col2 = st.columns(2)
    
    for idx, badge in enumerate(badges):
        # Alternate columns
        col = b_col1 if idx % 2 == 0 else b_col2
        
        with col:
            if badge['unlocked']:
                st.success(f"**🏅 {badge['name']}**\n\n*{badge['description']}*")
            else:
                # Dim/grayed out for locked badges
                st.markdown(f"""
                <div style="opacity: 0.5; border: 1px dashed gray; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <strong>🔒 {badge['name']}</strong><br>
                    <em>{badge['description']}</em>
                </div>
                """, unsafe_allow_html=True)
                
    st.divider()
    st.write(f"**Total Quizzes Completed:** {profile['quizzes_completed']}")