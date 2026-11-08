import streamlit as st
import base64
import os
from database.db import init_db, get_all_lectures

from ui.upload_page import render_upload_page
from ui.summary_page import render_summary_page
from ui.flashcard_page import render_flashcard_page
from ui.quiz_page import render_quiz_page
from ui.dashboard import render_dashboard_page

init_db()

def load_image_as_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def inject_custom_css():
    bg_base64 = load_image_as_base64(os.path.join("images", "bg.jpg"))
    bg_css = f'background-image: url("data:image/jpeg;base64,{bg_base64}");' if bg_base64 else 'background: #121212;'

    custom_css = f"""
    <style>
    /* 1. Global Background Setup */
    .stApp {{
        {bg_css}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    header[data-testid="stHeader"] {{ background: transparent !important; box-shadow: none !important; }}
    
    /* 2. Full-Screen Dark Overlay */
    .stApp::before {{
        content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px); z-index: 0;
    }}
    .stApp > div {{ z-index: 1; position: relative; }}
    
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp label, .stApp div {{
        color: #ffffff !important; text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }}
    div.block-container {{ padding-top: 2rem !important; }}

    /* =========================================================
       3. HORIZONTAL TOP NAV BAR (LIQUID GLASS) 
       ========================================================= */
    div[data-testid="stHorizontalBlock"]:first-of-type {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 50px;
        padding: 5px 30px;
        align-items: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }}
    
    /* =========================================================
       RADIO BUTTON CSS FIX (VERTICAL QUIZ CHOICES)
       ========================================================= */
    /* Aggressively hide the native radio dots everywhere */
    div[data-testid="stRadio"] div[role="radio"] > div:first-child,
    div[data-testid="stRadio"] div[data-baseweb="radio"] > div:first-child {{
        display: none !important; width: 0 !important; height: 0 !important; opacity: 0 !important;
    }}
    div[data-testid="stRadio"] input[type="radio"] {{ display: none !important; }}
    div.row-widget.stRadio {{ margin: 0 !important; padding: 0 !important; }}
    div.row-widget.stRadio > div {{ padding: 0 !important; border: none !important; background: transparent !important; }}

    /* Convert ONLY the Navbar Radio Group to a Horizontal Row */
    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] {{
        display: flex; flex-direction: row; justify-content: flex-end; gap: 35px; width: 100%; background: transparent;
    }}
    
    /* Make standard radio buttons (like Quiz and Login) stack vertically */
    section[data-testid="stMain"] div[role="radiogroup"]:not(div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"]) {{
        display: flex; flex-direction: column; gap: 12px; width: 100%;
    }}

    /* Active State styling for Quiz/Login Radio options (since dots are hidden) */
    section[data-testid="stMain"] div[role="radiogroup"]:not(div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"]) label:has(input:checked) {{
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px;
        padding: 10px !important;
        border-left: 3px solid #ffffff;
    }}
    section[data-testid="stMain"] div[role="radiogroup"]:not(div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"]) label {{
        padding: 10px !important;
        transition: all 0.3s ease;
    }}
    
    /* Style the Navigation Tabs specifically */
    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] label {{
        cursor: pointer; position: relative; padding: 10px 0px; margin: 0; background: transparent !important;
    }}
    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] label p {{
        font-size: 16px; font-weight: 500; color: #aaaaaa !important; transition: color 0.3s ease; margin: 0;
    }}
    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] label:hover p {{ color: #ffffff !important; }}
    
    /* Active Nav Tab Text Styling */
    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] label:has(div[aria-checked="true"]) p,
    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] label:has(input:checked) p {{
        color: #ffffff !important; font-weight: 700; text-shadow: 0 0 10px rgba(255,255,255,0.5);
    }}

    /* =========================================================
       4. SIDEBAR FOLDER SYSTEM & GENERAL UI
       ========================================================= */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 15, 15, 0.4) !important;
        backdrop-filter: blur(5px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.15);
    }}
    [data-testid="stSidebar"] .stButton > button {{
        width: 100%; justify-content: flex-start; text-align: left;
        background: transparent !important; border: none !important; box-shadow: none !important;
        border-radius: 8px !important; padding: 10px 15px !important; color: #ccc !important; font-weight: 400 !important;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.1) !important; color: white !important; transform: none !important;
    }}
    .stTextInput input, .stSelectbox > div > div > select, .stTextArea textarea {{
        background-color: rgba(255, 255, 255, 0.08) !important; backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important; border-radius: 10px !important; color: white !important;
    }}
    .stTextInput input:focus, .stSelectbox > div > div > select:focus {{ border: 1px solid rgba(255, 255, 255, 0.6) !important; }}
    
    div[data-testid="stMetric"], div[data-testid="stExpander"] {{
        background: rgba(255, 255, 255, 0.08) !important; backdrop-filter: blur(15px) !important;
        border-radius: 12px !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; padding: 15px !important;
    }}
    section[data-testid="stMain"] .stButton > button {{
        background: rgba(255, 255, 255, 0.1) !important; border: 1px solid rgba(255, 255, 255, 0.25) !important;
        backdrop-filter: blur(10px) !important; border-radius: 10px !important; font-weight: 600 !important;
        transition: all 0.3s ease !important; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }}
    section[data-testid="stMain"] .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.25) !important; transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.5) !important;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# --- Button Callback Functions ---
def handle_nav_click(target_page):
    st.session_state['nav_radio'] = target_page
    st.session_state['global_notification'] = None

def dismiss_notification():
    st.session_state['global_notification'] = None

def main():
    st.set_page_config(page_title="LectureMind", page_icon="💡", layout="wide", initial_sidebar_state="expanded")
    inject_custom_css()

    # --- HORIZONTAL LIQUID GLASS NAVBAR ---
    nav_col, = st.columns(1)
    with nav_col:
        pages_dict = {
            "Upload": render_upload_page,
            "Summary": render_summary_page,
            "Flashcards": render_flashcard_page,
            "Quiz": render_quiz_page,  # CHANGED FROM "Knowledge"
            "Dashboard": render_dashboard_page
        }
        
        if 'nav_radio' not in st.session_state:
            st.session_state['nav_radio'] = "Upload"
            
        st.radio("Navigation", list(pages_dict.keys()), horizontal=True, label_visibility="collapsed", key="nav_radio")

    # --- GLOBAL NOTIFICATION SYSTEM ---
    if st.session_state.get('global_notification'):
        notif = st.session_state['global_notification']
        st.success(f"✨ {notif['msg']}")
        
        c1, c2, _ = st.columns([2, 2, 6])
        with c1:
            st.button(f"🚀 Go to {notif['type']}", on_click=handle_nav_click, args=(notif['type'],))
        with c2:
            st.button("❌ Dismiss", on_click=dismiss_notification)
        st.divider()

    # --- SIDEBAR: LECTUREMIND LOGO & FOLDER BROWSER ---
    st.sidebar.markdown(
        "<div style='font-size: 26px; font-weight: 700; margin-bottom: 20px; color: white;'>💡 LectureMind</div>", 
        unsafe_allow_html=True
    )

    st.sidebar.title("📂 My Lectures")
    
    if 'user_id' in st.session_state:
        lectures = get_all_lectures(st.session_state['user_id'])
        if lectures:
            for lec in lectures:
                btn_label = f"📄 {lec['title']}"
                
                if st.sidebar.button(btn_label, key=f"lec_{lec['id']}"):
                    st.session_state['active_lecture_id'] = lec['id']
                    st.session_state['active_lecture_title'] = lec['title']
                    st.session_state.pop('temp_flashcards', None)
                    st.session_state.pop('temp_quiz', None)
                    st.session_state['global_notification'] = None
                    st.rerun()
        else:
            st.sidebar.info("No lectures saved yet. Upload an audio file to get started!")
        
        st.sidebar.divider()
        st.sidebar.write(f"👤 Logged in as: **{st.session_state['username']}**")
        if st.sidebar.button("Sign Out"):
            st.session_state.clear()
            st.rerun()
    else:
        st.sidebar.warning("Sign in via the Upload tab to view your folders.")

    # --- RENDER SELECTED PAGE ---
    pages_dict[st.session_state['nav_radio']]()

if __name__ == "__main__":
    main()