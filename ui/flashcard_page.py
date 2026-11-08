import streamlit as st
import os, json
from database.db import update_lecture_materials

def render_flashcard_page():
    st.title("📇 Interactive Flashcards")
    
    lecture_id = st.session_state.get('active_lecture_id')
    if not lecture_id:
        st.warning("Please open a lecture on the Upload page first.")
        return

    flashcards = st.session_state.get('temp_flashcards', [])
    
    if not flashcards:
        st.info("No active flashcards. Go to the Summary page to generate them.")
        return

    if 'fc_idx' not in st.session_state:
        st.session_state['fc_idx'] = 0
        st.session_state['fc_flipped'] = False
        st.session_state['fc_correct'] = 0
        st.session_state['fc_saved'] = False
        st.session_state['fc_warning'] = None

    idx = st.session_state['fc_idx']
    
    # --- END OF DECK LOGIC ---
    if idx >= len(flashcards):
        pct = (st.session_state['fc_correct'] / len(flashcards)) * 100
        if pct >= 60:
            st.success(f"🎉 You passed the test! Score: {pct:.0f}%")
            st.balloons()
        else:
            st.error(f"Keep practicing! Score: {pct:.0f}%")

        st.divider()
        
        if not st.session_state.get('fc_saved'):
            st.warning("⚠️ These flashcards haven't been saved yet.")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Save Flashcards"):
                    update_lecture_materials(lecture_id, flashcards=flashcards)
                    lec_title = st.session_state.get('active_lecture_title', 'unknown')
                    folder_dir = os.path.join("data", "lectures", lec_title)
                    os.makedirs(folder_dir, exist_ok=True)
                    fc_path = os.path.join(folder_dir, "flashcards.json")
                    with open(fc_path, "w") as f:
                        json.dump(flashcards, f, indent=4)
                        
                    st.session_state['fc_saved'] = True
                    st.session_state['fc_warning'] = None
                    st.rerun()

            with col2:
                if st.button("🔄 Retake (Without Saving)"): 
                    st.session_state['fc_warning'] = 'retake'
                    
            with col3:
                if st.button("✨ Generate New (Discard Current)"): 
                    st.session_state['fc_warning'] = 'new'
                
            if st.session_state.get('fc_warning'):
                st.error("Are you sure you want to discard these flashcards? They will be lost.")
                if st.button("Yes, I'm sure"):
                    if st.session_state['fc_warning'] == 'retake':
                        st.session_state['fc_idx'] = 0
                        st.session_state['fc_correct'] = 0
                        st.session_state['fc_warning'] = None
                        st.rerun()
                    else:
                        st.session_state['temp_flashcards'] = []
                        st.info("Discarded. Go to the Summary page to generate a new set.")
        else:
            st.success("✅ Flashcards are saved in your lecture folder.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Retake"):
                    st.session_state['fc_idx'] = 0
                    st.session_state['fc_correct'] = 0
                    st.rerun()
            with col2:
                if st.button("✨ Generate New (Clear Current)"):
                    st.session_state['temp_flashcards'] = []
                    st.session_state['fc_saved'] = False
                    st.rerun()
        return

    # --- ACTIVE CARD LOGIC (Dark Glass Theme) ---
    card = flashcards[idx]
    st.markdown(f"### Card {idx + 1} of {len(flashcards)}")
    
    st.markdown("""
        <style>
        .fc-box { 
            border: 1px solid rgba(255, 255, 255, 0.2); 
            border-radius: 16px; 
            padding: 40px; 
            text-align: center; 
            font-size: 24px; 
            font-weight: bold; 
            background: rgba(255, 255, 255, 0.1); 
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            color: #ffffff; 
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            min-height: 200px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    if not st.session_state['fc_flipped']:
        st.markdown(f"<div class='fc-box'>🤔 {card['question']}</div>", unsafe_allow_html=True)
        if st.button("🔄 Flip Card"):
            st.session_state['fc_flipped'] = True
            st.rerun()
    else:
        st.markdown(f"<div class='fc-box'>💡 {card['answer']}</div>", unsafe_allow_html=True)
        st.write("Did you get it right?")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Yes (Correct)"):
                st.session_state['fc_correct'] += 1
                st.session_state['fc_flipped'] = False
                st.session_state['fc_idx'] += 1
                st.rerun()
        with c2:
            if st.button("❌ No (Incorrect)"):
                st.session_state['fc_flipped'] = False
                st.session_state['fc_idx'] += 1
                st.rerun()