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
st.set_page_config(page_title="Understand your favorite artists' lyrics", page_icon="🎤", layout="wide")
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
    title     = "Unpack the stories behind your favourite artist 🎙️",
    subtitle  = "Pick an artist → we’ll scan their catalogue and reveal the "
                "<b>three&nbsp;main&nbsp;themes</b> running through their lyrics.",
    btn_text  = None,
    link      = None,
)

urls = get_urls()
THEMES_URL = urls.get('themes_url', '')
ARTISTS_URL = urls.get('artist_url', '')


# --- Récupération de la liste d’artistes (1 h de cache) ------------------
@st.cache_data(ttl=3_600, show_spinner="Loading artist list…")
def fetch_artists():
    res = get_request(ARTISTS_URL)
    if res and "results" in res:
        return sorted(res["results"])
    return []

artist_list = fetch_artists()


# ----------- Reset callbacks --------------------------------------------------
def reset_on_artist_change():
    st.session_state.artist_themes = None


# ----------- UI ---------------------------------------------------------------
st.divider()

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
    placeholder = "-"
    index = artist_list.index(st.session_state.artist_choice) if st.session_state.artist_choice else None
    artist_sel  = st.selectbox("🎧  Select an artist",
                                artist_list,
                                placeholder=placeholder,
                                index = index,
                                on_change=reset_on_artist_change)

    st.session_state.artist_choice = artist_sel
else:
    st.session_state.artist_choice = (
        st.text_input("🎧  Type an artist").strip() or None
    )

# --- CSS pour styliser le bouton désactivé ---
st.markdown("""
    <style>
    button[disabled] {
        border: 1px solid #CCCCCC !important;
        color: #AAAAAA !important;
        opacity: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)

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

# ----------  Séparateur  -----------------------------------------
st.markdown(
    "<hr style='border:none;border-top:1px solid #333;margin-top:1.5rem;'>",
    unsafe_allow_html=True,
)

# ----------  Toggle avec capture d'écran --------------------------------------
with st.expander("👀 Under the hood"):
    st.image(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'media/feature_1.png'), caption="Methodology feature 1", use_container_width=True)
