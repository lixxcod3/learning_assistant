import streamlit as st

def render_flashcard_page():
    st.title("📇 Flashcards")
    
    # Check if data exists
    if 'ai_materials' not in st.session_state:
        st.warning("No data found. Please go to the Upload page and process a file first.")
        return

    flashcards = st.session_state['ai_materials'].get('flashcards', [])
    
    if not flashcards:
        st.info("No flashcards generated for this lecture.")
        return

    # Initialize index in session state to track the current card
    if 'fc_index' not in st.session_state:
        st.session_state['fc_index'] = 0

    current_index = st.session_state['fc_index']
    total_cards = len(flashcards)
    
    # Get current card
    card = flashcards[current_index]

    # Flashcard UI
    st.markdown(f"### Card {current_index + 1} of {total_cards}")
    
    # The Question
    st.info(f"**Q: {card['question']}**")

    # The Answer (Hidden by default)
    with st.expander("👀 Reveal Answer"):
        st.success(f"A:")

    st.divider()

    # Navigation Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Previous", disabled=(current_index == 0)):
            st.session_state['fc_index'] -= 1
            st.rerun()
            
    with col3:
        if st.button("Next ➡️", disabled=(current_index == total_cards - 1)):
            st.session_state['fc_index'] += 1
            st.rerun()