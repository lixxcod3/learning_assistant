import streamlit as st

# Initialize database
from database.db import init_db

# Import UI pages
from ui.upload_page import render_upload_page
from ui.summary_page import render_summary_page
from ui.flashcard_page import render_flashcard_page
from ui.quiz_page import render_quiz_page
from ui.dashboard import render_dashboard_page

# Ensure database tables exist before the app renders
init_db()

def main():
    # Configure the main Streamlit window
    st.set_page_config(
        page_title="LectureMind",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.sidebar.title("🧠 LectureMind")
    st.sidebar.write("Your AI-powered learning companion.")
    st.sidebar.divider()

    # Define the navigation menu
    pages = {
        "🎙️ Upload & Process": render_upload_page,
        "📝 Lecture Summary": render_summary_page,
        "📇 Flashcards": render_flashcard_page,
        "🎮 Knowledge Quiz": render_quiz_page,
        "👤 My Dashboard": render_dashboard_page
    }

    # Sidebar radio button for navigation
    selection = st.sidebar.radio("Navigation", list(pages.keys()))

    st.sidebar.divider()
    st.sidebar.info("💡 **Tip:** Start by uploading a file. If you haven't uploaded anything, the other pages will ask you to go back!")

    # Execute the function for the selected page
    pages[selection]()

if __name__ == "__main__":
    main()