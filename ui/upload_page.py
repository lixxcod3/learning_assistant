import streamlit as st
import tempfile, os, re, json
from audio.extractor import extract_audio
from audio.transcriber import transcribe_audio
from ai.summarizer import generate_summary
from ai.key_points import generate_key_points
from database.db import save_lecture_initial, verify_login, create_user, check_user_exists

def render_upload_page():
    # --- AUTHENTICATION CHECK ---
    if 'user_id' not in st.session_state:
        st.title("🔒 Sign In")
        st.warning("⚠️ You must be signed in to process files and save your progress.")
        
        auth_mode = st.radio("Select an option:", ["Login", "Create Account"], horizontal=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Submit"):
            if auth_mode == "Login":
                if not check_user_exists(username):
                    st.error("Username not found. Please select 'Create Account'.")
                else:
                    uid = verify_login(username, password)
                    if uid:
                        st.session_state['user_id'] = uid
                        st.session_state['username'] = username
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
            else:
                uid = create_user(username, password)
                if uid:
                    st.session_state['user_id'] = uid
                    st.session_state['username'] = username
                    st.success("Account created successfully!")
                    st.rerun()
                else:
                    st.error("Username already exists.")
        return 
    
    # --- NEW UPLOAD LOGIC ---
    st.title("🎙️ Upload Lecture Audio")
    st.markdown("Create a new AI-powered study session from your audio file.")
    
    lecture_title = st.text_input("Lecture Title")
    uploaded_file = st.file_uploader("Choose a file", type=["mp3", "mp4", "wav"])
    
    if uploaded_file is not None and lecture_title:
        if st.button("Process Audio & Generate Summary"):
            safe_title = re.sub(r'[^a-zA-Z0-9_\- ]', '', lecture_title).strip()
            lecture_dir = os.path.join("data", "lectures", safe_title)
            os.makedirs(lecture_dir, exist_ok=True)
            
            orig_path = os.path.join(lecture_dir, uploaded_file.name)
            with open(orig_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            with st.spinner("Extracting audio & transcribing..."):
                wav_path = extract_audio(orig_path)
                transcript_data = transcribe_audio(wav_path)
                segments = transcript_data.get('segments', [])
                full_text = " ".join([seg['text'] for seg in segments])
                os.remove(wav_path)
            
            with st.spinner("Generating summary and key points..."):
                summary_data = generate_summary(full_text)
                key_points_data = generate_key_points(full_text)
                
                lm_path = os.path.join(lecture_dir, "learning_material.json")
                with open(lm_path, "w") as f:
                    json.dump({"summary": summary_data, "key_points": key_points_data}, f, indent=4)
                
                lecture_id = save_lecture_initial(
                    user_id=st.session_state['user_id'],
                    title=safe_title, transcript=full_text,
                    summary=summary_data.get("detailed_summary", ""),
                    key_points=key_points_data.get("key_points", [])
                )
                st.session_state['active_lecture_id'] = lecture_id
                st.session_state['active_lecture_title'] = safe_title
                
            st.success("✨ Folder created and summary saved! Go to the Summary tab.")