import streamlit as st

def render_summary_page():
    st.title("📝 Lecture Summary")
    
    # Check if data exists in session state
    if 'ai_materials' not in st.session_state or 'transcript' not in st.session_state:
        st.warning("No data found. Please go to the Upload page and process a file first.")
        return

    # Fetch data from session state
    materials = st.session_state['ai_materials']
    transcript = st.session_state['transcript']

    # Display Summary
    st.header("Executive Summary")
    st.info(materials.get("summary", "No summary available."))

    st.divider()

    # Display Key Points
    st.header("🔑 Key Points")
    key_points = materials.get("key_points", [])
    if key_points:
        for point in key_points:
            st.markdown(f"- {point}")
    else:
        st.write("No key points extracted.")

    st.divider()

    # Display Full Transcript inside an expander
    st.header("📄 Full Transcript")
    with st.expander("Click to view full transcript"):
        st.write(transcript.get("full_text", "No transcript available."))
        
        # Optional: Display timestamped segments if they exist
        st.markdown("### Timestamped Segments")
        segments = transcript.get("segments", [])
        for seg in segments:
            st.caption(f"[{seg['start']}s - {seg['end']}s] {seg['text']}")