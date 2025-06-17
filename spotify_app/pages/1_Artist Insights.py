# --------------------------PARAMS & IMPORT-------------------------------------
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils import get_request, display_themes, get_urls
from spotify_style import apply as apply_style
# ------------------------------------------------------------------------------

# ----------- Streamlit config & style------------------------------------------
st.set_page_config(page_title="Understand your favorite artists' lyrics", page_icon="🎤", layout="wide")
apply_style()

urls = get_urls()
THEMES_URL = urls.get('themes_url', '')
ARTISTS_URL = urls.get('artist_url', '')

# ---------- State init---------------------------------------------------------
for k in ("artist_themes", "artist_choice"):
    st.session_state.setdefault(k, None)

# --- Récupération de la liste d’artistes (1 h de cache) ------------------
@st.cache_data(ttl=3_600, show_spinner="Loading artist list…")
def fetch_artists():
    res = get_request(ARTISTS_URL)
    if res and "results" in res:
        return sorted(res["results"])
    return []

artist_list = fetch_artists()

# ----------------- Intro-------------------------------------------------------
st.markdown(
    """
    <div style="max-width:900px;margin:auto">
      <h1 style="margin-bottom:0">
        Unpack the stories behind your favourite artist 🎙️
      </h1>
      <p style="opacity:0.8;margin-top:0.25rem">
        Pick an artist&nbsp;→&nbsp;we’ll scan their catalogue and reveal the
        <b>three&nbsp;main&nbsp;themes</b> running through their lyrics.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# ---------------- Layout ---------------------------------------------
st.markdown(
    """
    <style>
    .artist-card{background:#191414;
    padding:0.5rem 1.5rem 0.5em;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="artist-card">', unsafe_allow_html=True)

# --- Select box (ou input) ----------------------------------------
if artist_list:
        placeholder = "—"
        artist_sel  = st.selectbox("🎧  Select an artist",
                                   [placeholder] + artist_list,
                                   index=0)
        st.session_state.artist_choice = None if artist_sel == placeholder else artist_sel
else:
        st.session_state.artist_choice = (
            st.text_input("🎧  Type an artist").strip() or None
        )

# --- Bouton -------------------------------------------------------
clicked = st.button("Find themes ", use_container_width=True,
                 disabled=st.session_state.artist_choice is None)
if clicked :
        with st.spinner("Generating…"):
            res = get_request(THEMES_URL,
                              params={"input": st.session_state.artist_choice})
        if res:
            st.session_state.artist_themes = res
        else:
            st.error("Couldn't retrieve themes from API")

st.markdown("</div>", unsafe_allow_html=True)


# --- Affichage ----------------------------------------------------------------
if st.session_state.artist_themes:
    st.divider()
    display_themes(st.session_state.artist_themes, artist=st.session_state.artist_choice)
