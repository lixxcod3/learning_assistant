import streamlit as st
import base64
import os
from database.db import init_db, get_all_lectures_full

from ui.upload_page import render_upload_page
from ui.summary_page import render_summary_page
from ui.flashcard_page import render_flashcard_page
from ui.quiz_page import render_quiz_page
from ui.dashboard import render_dashboard_page
from ui.components import render_lecture_folder

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
    /* =========================================================
       ULTRA-CLEAN NOTION FOLDER ITEMS
       ========================================================= */
    div[data-testid="stExpanderDetails"] div[data-testid="stVerticalBlock"] {{
        gap: 0.1rem !important; 
    }}
    
    /* Strip ALL backgrounds, borders, and shadows from buttons inside folders */
    div[data-testid="stExpanderDetails"] .stButton > button {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        height: auto !important;
        min-height: 32px !important;
        padding: 4px 8px !important;
        border-radius: 4px !important;
        font-weight: 400 !important;
        color: #cccccc !important;
        justify-content: flex-start !important; 
    }}
    
    div[data-testid="stExpanderDetails"] .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
    }}
    
    /* =========================================================
       GENERAL UI 
       ========================================================= */
    .stApp {{
        {bg_css}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    header[data-testid="stHeader"] {{ background: transparent !important; box-shadow: none !important; }}
    
    .stApp::before {{
        content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px); z-index: 0;
    }}
    .stApp > div {{ z-index: 1; position: relative; }}
    
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp label, .stApp div {{
        color: #ffffff !important; text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }}
    div.block-container {{ padding-top: 2rem !important; }}

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
    
    div[data-testid="stRadio"] div[role="radio"] > div:first-child,
    div[data-testid="stRadio"] div[data-baseweb="radio"] > div:first-child {{
        display: none !important; width: 0 !important; height: 0 !important; opacity: 0 !important;
    }}
    div[data-testid="stRadio"] input[type="radio"] {{ display: none !important; }}
    div.row-widget.stRadio {{ margin: 0 !important; padding: 0 !important; }}
    div.row-widget.stRadio > div {{ padding: 0 !important; border: none !important; background: transparent !important; }}

    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] {{
        display: flex; flex-direction: row; justify-content: flex-end; gap: 35px; width: 100%; background: transparent;
    }}
    
    section[data-testid="stMain"] div[role="radiogroup"]:not(div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"]) {{
        display: flex; flex-direction: column; gap: 12px; width: 100%;
    }}

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
    
    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] label {{
        cursor: pointer; position: relative; padding: 10px 0px; margin: 0; background: transparent !important;
    }}
    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] label p {{
        font-size: 16px; font-weight: 500; color: #aaaaaa !important; transition: color 0.3s ease; margin: 0;
    }}
    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] label:hover p {{ color: #ffffff !important; }}
    
    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] label:has(div[aria-checked="true"]) p,
    div[data-testid="stHorizontalBlock"]:first-of-type div[role="radiogroup"] label:has(input:checked) p {{
        color: #ffffff !important; font-weight: 700; text-shadow: 0 0 10px rgba(255,255,255,0.5);
    }}

    [data-testid="stSidebar"] {{
        background-color: rgba(15, 15, 15, 0.4) !important;
        backdrop-filter: blur(5px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.15);
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

def handle_nav_click(target_page):
    st.session_state['nav_radio'] = target_page

def main():
    st.set_page_config(page_title="LectureMind", page_icon="💡", layout="wide", initial_sidebar_state="expanded")
    inject_custom_css()

    nav_col, = st.columns(1)
    with nav_col:
        pages_dict = {
            "Upload": render_upload_page,
            "Summary": render_summary_page,
            "Flashcards": render_flashcard_page,
            "Quiz": render_quiz_page, 
            "Dashboard": render_dashboard_page
        }
        
        if 'nav_radio' not in st.session_state:
            st.session_state['nav_radio'] = "Upload"
            
        st.radio("Navigation", list(pages_dict.keys()), horizontal=True, label_visibility="collapsed", key="nav_radio")

    st.sidebar.markdown(
        "<div style='font-size: 26px; font-weight: 700; margin-bottom: 20px; color: white;'>💡 LectureMind</div>", 
        unsafe_allow_html=True
    )

    st.sidebar.title("📂 My Lectures")
    
    if 'user_id' in st.session_state:
        lectures = get_all_lectures_full(st.session_state['user_id'])
        
        if lectures:
            with st.sidebar: 
                for lec in lectures[:10]:
                    render_lecture_folder(lec, prefix="side")
                
            if len(lectures) > 10:
                st.sidebar.divider()
                st.sidebar.button(
                    f"Show More ({len(lectures) - 10} hidden)", 
                    use_container_width=True, 
                    on_click=handle_nav_click, 
                    args=("Dashboard",)
                )
        else:
            st.sidebar.info("No lectures saved yet. Upload an audio file to get started!")
        
        st.sidebar.divider()
        st.sidebar.write(f"👤 Logged in as: **{st.session_state['username']}**")
        if st.sidebar.button("Sign Out"):
            st.session_state.clear()
            st.rerun()
    else:
        st.sidebar.warning("Sign in via the Upload tab to view your folders.")

    pages_dict[st.session_state['nav_radio']]()

if __name__ == "__main__":
    main()