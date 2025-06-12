import streamlit as st

st.set_page_config(page_title="AI Spotify Lyrics", page_icon="🐍", layout="wide")

# No sidebar radio — rely on Streamlit built-in page switcher

# Centered welcome text using columns
col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    st.title("Welcome to AI Spotify Lyrics")
    st.markdown("""
    This app helps you:
    - Get top themes by artists
    - Get recommended songs based on your mood
    - Get recommended songs based on a song

    Use the built-in page switcher in the sidebar to navigate between pages.
    """)
