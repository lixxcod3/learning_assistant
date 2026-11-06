python -c "from pathlib import Path; p=Path('ui/summary_page.py'); p.write_text('''import streamlit as st

def render_summary_page():
    st.title('Lecture Summary')

    if 'ai_materials' not in st.session_state or 'transcript' not in st.session_state:
        st.warning('No data found. Please go to the Upload page and process a file first.')
        return

    materials = st.session_state['ai_materials']
    transcript = st.session_state['transcript']

    st.header('Executive Summary')
    st.info(materials.get('summary', 'No summary available.'))

    st.divider()

    st.header('Key Points')
    key_points = materials.get('key_points', [])

    if key_points:
        for point in key_points:
            st.markdown(f'- {point}')
    else:
        st.write('No key points extracted.')

    st.divider()

    st.header('Full Transcript')

    with st.expander('Click to view full transcript'):
        st.write(transcript.get('full_text', 'No transcript available.'))

        st.markdown('### Timestamped Segments')
        segments = transcript.get('segments', [])

        for seg in segments:
            st.caption(f\\\"[{seg['start']}s - {seg['end']}s] {seg['text']}\\\")
''', encoding='utf-8'); print('File successfully written! Lines:', len(p.read_text(encoding='utf-8').splitlines()))"