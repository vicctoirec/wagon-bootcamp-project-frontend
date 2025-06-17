import streamlit as st

_SPOTIFY_GREEN = "#1DB954"

_CSS = f"""
<style>
/* ---- fond & texte global ---- */
.stApp {{ background:#191414; color:#FFFFFF; }}

/* ---- bouton principal ---- */
div.stButton>button {{
    background:{_SPOTIFY_GREEN}; color:#FFFFFF; border:none;
    padding:.5rem 1.2rem; border-radius:9999px; font-weight:700;
}}
div.stButton>button:hover {{ background:#1ed760; }}

/* ---- zones de texte (textarea + text_input) ---- */
textarea, textarea:focus,
input[type="text"], input[type="text"]:focus {{
    background:#121212 !important;
    color:#FFFFFF !important;
    border:1px solid #3a3a3a !important;      /* léger contour gris */
}}

/* ---- placeholders ---- */
textarea::placeholder,
input::placeholder {{
    color:#888888 !important;
    opacity:1;
}}

/* Sidebar highlight */
section[data-testid="stSidebar"] > div:first-child {{
    background:#0d0d0d;}}


/* ---- labels & titres ---- */
label, h1, h2, h3, h4, h5, h6, p {{
    color:#FFFFFF !important;
}}
</style>
"""

def apply():
    """Injecte la feuille de style Spotify-dark dans la page courante."""
    st.markdown(_CSS, unsafe_allow_html=True)
