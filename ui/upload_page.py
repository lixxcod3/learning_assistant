import streamlit as st
import tempfile
import os
import re
import json
import shutil

from audio.extractor import extract_audio
from audio.transcriber import transcribe_audio
from ai.summarizer import generate_summary
from ai.key_points import generate_key_points
from database.db import save_lecture_initial, get_all_lectures

def render_upload_page():
    st.title("🎙️ Lecture Manager & Upload")
    
    lectures = get_all_lectures()
    if lectures:
        st.subheader("📂 Open Existing Lecture")
        options = {lec['id']: lec['title'] for lec in lectures}
        selected_id = st.selectbox("Select a saved lecture:", list(options.keys()), format_func=lambda x: options[x])
        if st.button("Load Lecture"):
            st.session_state['active_lecture_id'] = selected_id
            st.session_state['active_lecture_title'] = options[selected_id]
            st.success(f"Loaded '{options[selected_id]}'. Go to Summary or Flashcards!")
    
    st.divider()
    st.subheader("➕ Create New Lecture")
    lecture_title = st.text_input("Lecture Title (Required to save without overlapping)")
    uploaded_file = st.file_uploader("Choose a file", type=["mp3", "mp4", "wav"])
    
    if uploaded_file is not None and lecture_title:
        if st.button("Process Audio & Generate Summary"):
            safe_title = re.sub(r'[^a-zA-Z0-9_\- ]', '', lecture_title).strip()
            lecture_dir = os.path.join("data", "lectures", safe_title)
            os.makedirs(lecture_dir, exist_ok=True)
            
            # Save Original File
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
                
                # Save Learning Material JSON to folder
                lm_path = os.path.join(lecture_dir, "learning_material.json")
                with open(lm_path, "w") as f:
                    json.dump({"summary": summary_data, "key_points": key_points_data}, f, indent=4)
                
                lecture_id = save_lecture_initial(
                    title=safe_title,
                    transcript=full_text,
                    summary=summary_data.get("detailed_summary", ""),
                    key_points=key_points_data.get("key_points", [])
                )
                st.session_state['active_lecture_id'] = lecture_id
                st.session_state['active_lecture_title'] = safe_title
                
            st.success("✨ Folder created and summary saved! Go to the Summary page.")