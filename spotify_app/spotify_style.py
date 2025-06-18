import streamlit as st
from uuid import uuid4

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


# ── 2️⃣  Re-usable “hero” banner  ──────────────────────────────────
def hero(title:str, subtitle:str, btn_text:str|None=None, link:str|None=None):
    # a random id so multiple banners on the same page don’t collide
    hid = uuid4().hex[:6]
    st.markdown(
        f"""
        <style>
        .hero-{hid} {{
            background:linear-gradient(135deg,#1DB954 0%,#0d1 55%,#000 100%);
            padding:3rem 3rem 2.5rem;border-radius:12px;box-shadow:0 0 20px #0006;
        }}
        .hero-{hid} h1{{margin:0 0 .5rem 0;font-size:2.6rem;line-height:1.1}}
        .hero-{hid} p{{margin:.5rem 0 1.25rem 0;opacity:.85}}
        .hero-{hid} a.button{{display:inline-block;background:#1DB954;
            color:#fff;font-weight:600;padding:.55rem 1.5rem;border-radius:9999px;
            text-decoration:none}}
        .hero-{hid} a.button:hover{{background:#1ed760}}
        </style>

        <div class="hero-{hid}">
            <h1>{title}</h1>
            <p>{subtitle}</p>
            {f'<a class="button" href="{link}">{btn_text}&nbsp;↓</a>' if btn_text and link else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )
