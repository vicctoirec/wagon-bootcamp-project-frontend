import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils import get_request, display_songs, spotify_player, get_urls

if "mood_songs" not in st.session_state:
    st.session_state["mood_songs"] = None

st.header("Find songs matching your mood")

mood = st.text_area(
    "Pitch your mood",
    placeholder="I'm going on vacation to Italy with my best friend..."
)

urls = get_urls()
MOOD_URL = urls.get('mood_url', '')

if st.button("Find songs", key="mood-btn"):
    if not mood.strip():
        st.warning("Please enter a mood description!")
    else:
        result = get_request(MOOD_URL, mood)
        if result and 'prediction' in result:
            st.session_state["mood_songs"] = result['prediction']
        else:
            st.warning("No songs found or API error.")

if st.session_state["mood_songs"]:
    display_songs({"prediction": st.session_state["mood_songs"]})
    spotify_player(st.session_state["mood_songs"])
