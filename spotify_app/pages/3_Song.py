import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils import get_request, display_songs, spotify_player, get_urls

st.set_page_config(page_title="Find Similar Songs", page_icon="🐍🎵", layout="wide")

if "song_songs" not in st.session_state:
    st.session_state["song_songs"] = None

st.header("Find songs matching your song")

song = st.text_input("Search a song", placeholder="Smoke Two Joints")

urls = get_urls()
SONG_URL = urls.get('song_url', '')

if st.button("Find songs", key="song-btn"):
    if not song.strip():
        st.warning("Please enter a song name!")
    else:
        result = get_request(SONG_URL, song)
        if result and 'prediction' in result:
            st.session_state["song_songs"] = result['prediction']
        else:
            st.warning("No songs found or API error.")

if st.session_state["song_songs"]:
    display_songs({"prediction": st.session_state["song_songs"]})
    spotify_player(st.session_state["song_songs"])
