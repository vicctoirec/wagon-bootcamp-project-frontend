import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils import get_request, display_themes, get_urls

st.set_page_config(page_title="Understand Artists' Lyrics", page_icon="🐍🎵", layout="wide")


if "artist_themes" not in st.session_state:
    st.session_state["artist_themes"] = None

st.header("Discover your artist")

artist = st.text_input("Search an artist", placeholder="Johnny Cash")

urls = get_urls()
THEMES_URL = urls.get('themes_url', '')

if st.button("Find themes", key="artist-btn"):
    if not artist.strip():
        st.warning("Please enter an artist name!")
    else:
        result = get_request(THEMES_URL, artist)
        if result:
            st.session_state["artist_themes"] = result

if st.session_state["artist_themes"]:
    display_themes(st.session_state["artist_themes"])
