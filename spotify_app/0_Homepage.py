# spotify_app/pages/0_Home.py
"""
🎧  Spotify-style landing page
────────────────────────────
Affiche la “home” dynamique (trending tracks / new releases / popular artists)
et rappelle les trois features de l’app.
"""

import streamlit as st
from spotify_style import apply           # thème global dark spotify

# -- 1️⃣  THEME ----------------------------------------------------------------
st.set_page_config(page_title="AI Spotify Lyrics", page_icon="🎧", layout="wide")
apply()

# -- 2️⃣  TITRE ----------------------------------------------------------------
st.title("Welcome to AI Spotify Lyrics")
st.write("We’ve built **3 features** to help you fine-tune your music choices thanks to lyrics.")

st.write("Use the page switcher in the sidebar to navigate between features.")

# -- 3️⃣  FEATURES CARDS + EXPANDERS -------------------------------------------

# Première ligne : titres
fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    st.markdown("**🎶 Feature 1: Discover Top Themes in Your Favorite Artist's Lyrics**")
with fcol2:
    st.markdown("**😊 Feature 2: Get Song Recommendations Based on Your Mood**")
with fcol3:
    st.markdown("**🔥 Feature 3: Find Songs Similar to Your Favorite Track**")

# Deuxième ligne : expanders
ecol1, ecol2, ecol3 = st.columns(3)
with ecol1:
    with st.expander("More info"):
        st.markdown(
            "- 🎤 **Enter your favorite artist’s name**\n"
            "- 🔍 **Uncover the main themes and stories behind their lyrics**\n"
            "- ▶️ **Listen to your artist’s top songs right here in the app**"
        )
with ecol2:
    with st.expander("More info"):
        st.markdown(
            "- 📝 **Tell us how you’re feeling today**\n"
            "- ✍️ **Receive a brief, personalized mood description**\n"
            "- 🎧 **Enjoy a curated 5-song playlist that perfectly matches your vibe**\n"
            "- ▶️ **Play the playlist seamlessly within the app**"
        )
with ecol3:
    with st.expander("More info"):
        st.markdown(
            "- 🎵 **Input your favorite song and artist**\n"
            "- 🎶 **Discover a 5-song playlist tailored to your preferred beats and lyrics**\n"
            "- ▶️ **Enjoy smooth playback right inside the app**"
        )

st.markdown("---")
