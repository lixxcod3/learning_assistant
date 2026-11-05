import streamlit as st
import time

def render_upload_page():
    st.title("🎙️ Upload Lecture / Podcast")
    st.write("Upload an audio or video file to generate smart learning materials.")
    
    # UI for file upload
    uploaded_file = st.file_uploader("Choose a file", type=["mp3", "mp4", "wav"])
    
    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        
        # When clicked, we simulate the backend processing
        if st.button("Generate Learning Materials"):
            
            # --- Simulating Person 1 (Audio & Transcription) ---
            with st.spinner("Extracting audio & transcribing... (Simulating Person 1)"):
                time.sleep(2) # Fake processing delay
                
                # Save mock transcript to session state so other pages can read it
                st.session_state['transcript'] = {
                    "full_text": "Artificial intelligence allows machines to perform tasks that typically require human intelligence. Machine learning is a powerful subset of AI.",
                    "segments": [
                        {"start": 0.0, "end": 4.5, "text": "Artificial intelligence allows machines to perform tasks"},
                        {"start": 4.5, "end": 9.0, "text": "that typically require human intelligence."},
                        {"start": 9.0, "end": 14.2, "text": "Machine learning is a powerful subset of AI."}
                    ]
                }
            
            # --- Simulating Person 2 (AI Generation) ---
            with st.spinner("Analyzing content & generating quizzes... (Simulating Person 2)"):
                time.sleep(2) # Fake processing delay
                
                # Save mock AI materials to session state
                st.session_state['ai_materials'] = {
                    "summary": "This lecture introduces artificial intelligence and highlights machine learning as a key subset.",
                    "key_points": [
                        "AI mimics human intelligence to perform tasks.",
                        "Machine learning is explicitly a subset of AI."
                    ],
                    "flashcards": [
                        {"question": "What is AI?", "answer": "Technology that allows machines to perform human-like intelligent tasks."},
                        {"question": "What is the relationship between AI and Machine Learning?", "answer": "Machine learning is a subset of AI."}
                    ],
                    "quiz": [
                        {
                            "question": "Which of the following is a subset of AI?",
                            "options": ["Cloud Computing", "Machine learning", "Data storage", "Web Development"],
                            "answer": "Machine learning",
                            "explanation": "The lecture explicitly states that machine learning is a powerful subset of AI."
                        }
                    ]
                }
                
            st.success("✨ Processing complete! Use the navigation menu to explore your learning materials.")