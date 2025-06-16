# --------------------------PARAMS & IMPORT-------------------------------------
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils import get_request, display_matching_songs, spotify_player, get_urls

urls = get_urls()
ENRICH_URL = urls.get('enriched_url', '')
MOOD_URL = urls.get('mood_url', '')
# -----------------------------------------------------------------------------



# ----------- Streamlit config & style------------------------------------------
spotify_green = "#1DB954"

st.set_page_config(page_title="Find Songs", page_icon="🎧", layout="wide")

st.markdown(f"""
<style>
/* ---- fond & texte global ---- */
.stApp {{ background:#191414; color:#FFFFFF; }}

/* ---- bouton principal ---- */
div.stButton>button {{
    background:{spotify_green}; color:#FFFFFF; border:none;
    padding:.5rem 1.2rem; border-radius:9999px; font-weight:700;
}}
div.stButton>button:hover {{ background:#1ed760; }}

/* ---- zone de texte ---- */
textarea, textarea:focus {{
    background:#121212 !important;
    color:#FFFFFF !important;
}}
textarea::placeholder {{
    color:#888888 !important;   /* gris clair */
    opacity:1;
}}

/* ---- labels & titres ---- */
label, h1, h2, h3, h4, h5, h6, p {{
    color:#FFFFFF !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------- State init---------------------------------------------------------
for k in ("raw", "enriched","predict-mood-songs", "loading_playlist"):
    if k == "loading_playlist":
        st.session_state.setdefault(k, False)
    else:
        st.session_state.setdefault(k, None)


# ---------- Input zone --------------------------------------------------------
st.header("Find songs matching your mood")
st.write("Describe your feelings or plans - AI will craft a vibe!")

st.session_state.raw = st.text_area(
    "Pitch your mood :",
    value=st.session_state.raw or "",
    height=100,
    placeholder="I'm going on vacation to Italy with my best friend…",
)

# ---------- STEP 1 : Enrich ---------------------------------------------------
if st.session_state.enriched is None:

    if st.button("Enrich my prompt"):

        raw = st.session_state.get("raw", "")
        if not raw.strip():
            st.warning("Please enter a mood description!")
        else:
            with st.spinner("Calling Gemini …"):
                result = get_request(ENRICH_URL, params={"user_input": raw})

                # ───────── Gestion du retour ─────────
                if result and "enriched_input" in result:
                    st.session_state.enriched = result["enriched_input"]
                else:
                    st.error("API error: could not retrieve enriched prompt.")


# ---------- STEP 2 : show enriched + actions ----------------------------------
if st.session_state.enriched:

    st.subheader("🎼 Your vibe")
    st.write(st.session_state.enriched)

    col_a, col_b = st.columns(2)

    # -- Regenerate ------------------------------------------------------------
    with col_a:
        if st.button("🔁 Regenerate"):
            with st.spinner("Regenerating… ⏳"):
                result = get_request(ENRICH_URL,
                                     params={"user_input": st.session_state.raw})

                if result and "enriched_input" in result:
                    st.session_state.enriched  = result["enriched_input"]
                    st.session_state['predict-mood-songs'] = None
                    st.rerun()
                else:
                    st.error("API error: could not regenerate prompt.")

    # -- Get playlist --------------------------------------------------------

    # bouton grisé si :
    #  ↳ aucun prompt enrichi
    #  ↳ un appel playlist est déjà en cours
        disabled = (not st.session_state.enriched or st.session_state.loading_playlist)

    with col_b:
        if st.button("🚀 Get playlist", disabled=disabled):
            st.session_state.loading_playlist = True
            with st.spinner("Building your playlist… ⏳"):
                result = get_request(MOOD_URL,
                                     params={"enriched_input": st.session_state.enriched})
            st.session_state.loading_playlist = False

            # Le back-end renvoie {"prediction": …}
            if result and "prediction" in result:
                st.session_state['predict-mood-songs'] = result["prediction"]
                st.rerun()
            else:
                st.error("API error: could not retrieve playlist.")

# ---------- STEP 3 : display playlist -----------------------------------------
if st.session_state['predict-mood-songs']:
    st.success("Here are your songs!")
    songs = st.session_state['predict-mood-songs']

    display_matching_songs(songs)
    spotify_player(songs)
