# --------------------------PARAMS & IMPORT-------------------------------------
import sys
import os
import base64
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils import get_request, display_themes, get_urls
from spotify_style import apply as apply_style, hero
# ------------------------------------------------------------------------------

# ----------- Streamlit config & style------------------------------------------
st.set_page_config(page_title="About us", page_icon="🤓", layout="wide")
apply_style()

# Convertir l'image en base64
with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'media/qr_code.jpg'), "rb") as f:
    img_data = f.read()
img_base64 = base64.b64encode(img_data).decode()

# Affichage centré dans la sidebar
st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{img_base64}" width="130"/>
        <p style="margin-top: 0.5rem;">Try the app!</p>
    </div>
    """,
    unsafe_allow_html=True
)

for k in ("artist_themes", "artist_choice", "sm_artist_choice", "sm_song_choice", "sm_song_songs", "sm_lyrics_explain"):
    if k not in st.session_state:
        st.session_state.setdefault(k, None)

hero(
    title     = "Get to know the team 🗣️",
    subtitle  = "Meet the genius individuals behind the features.",
    btn_text  = None,
    link      = None,
)

st.subheader("😎 This is us")

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
col1, col2, col3, col4 = st.columns(4)

def render_profile(col, img_path, name, bio, img_width=150):
    with col:
        st.image(img_path, width=img_width)
        st.markdown(f"#### {name}", unsafe_allow_html=True)
        st.markdown(bio, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

render_profile(
    col1,
    os.path.join(base_path, 'media/victoire.png'),
    "Victoire",
    "After five years in strategy consulting, she is taking a sabbatical to explore new skills, including coding and AI. She's passionate about how technology is reshaping the world and is considering returning to strategy or finance — or possibly launching her own venture."
)

render_profile(
    col2,
    os.path.join(base_path, 'media/jean.png'),
    "Jean",
    "With a background in IT project management and database development, he has experience as both MOA and MOE. He is now pivoting toward data engineering and AI, with a focus on technical project leadership and intelligent system development."
)

render_profile(
    col3,
    os.path.join(base_path, 'media/laureen.png'),
    "Laureen",
    "A former field test engineer at Decathlon, she combines expertise in product performance with a passion for football. After years coaching in professional women’s clubs, she’s now learning to code to build tools that empower athletes and aims to merge tech and sport through innovative, data-driven solutions."
)

render_profile(
    col4,
    os.path.join(base_path, 'media/margaux.png'),
    "Margaux",
    "She has worked as a data analyst in tech for eight years and is now deepening her technical expertise through a data science bootcamp, aiming to take on more advanced roles in the data and AI space."
)
