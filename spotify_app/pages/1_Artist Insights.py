# --------------------------PARAMS & IMPORT-------------------------------------
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils import get_request, display_themes, get_urls
from spotify_style import apply as apply_style

urls = get_urls()
THEMES_URL = urls.get('themes_url', '')
ARTISTS_URL = urls.get('artist_url', '')
# ------------------------------------------------------------------------------

# ----------- Streamlit config & style------------------------------------------
st.set_page_config(page_title="Understand Artists' Lyrics", page_icon="🎧", layout="wide")
apply_style()


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

# --- Sélecteur (ou saisie libre si l’API ne répond pas) ------------------
st.header("Unpack the stories behind your favourite artist")

if artist_list:
    # Menu déroulant (avec une ligne « Select… » au début)
    placeholder = "Select an artist"
    choices     = [placeholder] + artist_list
    selection   = st.selectbox("Search an artist", choices, index=0)

    # Si l’utilisateur choisit un vrai artiste on le garde ; sinon None
    st.session_state.artist_choice = (
        None if selection == placeholder else selection
    )
else:
    # fallback : champ texte classique
    st.session_state.artist_choice = st.text_input(
        "Search an artist", placeholder="Johnny Cash"
    ).strip() or None


# --- Bouton « Find themes » ---------------------------------------------
if st.button("Find themes", key="artist-btn") and st.session_state.artist_choice:
    with st.spinner("Looking for themes…"):
        result = get_request(
            THEMES_URL,
            params={"input": st.session_state.artist_choice})
    st.session_state.artist_themes = result if result else None
    if not result:
        st.error("API error : could not retrieve themes.")

# --- 4️⃣  Affichage -----------------------------------------------------------
if st.session_state.artist_themes:
    display_themes(st.session_state.artist_themes)
