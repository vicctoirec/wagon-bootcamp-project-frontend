# --------------------------PARAMS & IMPORT-------------------------------------
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils import get_request, display_matching_songs, spotify_player, get_urls
from spotify_style import apply as apply_style

urls = get_urls()
ENRICH_URL = urls.get('enriched_url', '')
MOOD_URL = urls.get('mood_url', '')
# -----------------------------------------------------------------------------


# ----------- Streamlit config & style------------------------------------------
spotify_green = "#1DB954"

st.set_page_config(page_title="Find Songs", page_icon="🎧", layout="wide")

apply_style()

# ---------- State init---------------------------------------------------------
for k in ("raw", "enriched","predict-mood-songs", "loading_playlist"):
    if k == "loading_playlist":
        st.session_state.setdefault(k, False)
    else:
        st.session_state.setdefault(k, None)

# -------  HEADER -----------------------------------------------------------
st.markdown(
    """
    <div style="max-width:900px;margin:auto">
      <h1 style="margin-bottom:0">
        Turn today’s mood into the perfect playlist 🔥
      </h1>
      <p style="opacity:0.8;margin-top:0.25rem">
        Tell us how you feel&nbsp;→&nbsp;we’ll craft a tailor-made mix of
        <b>fresh tracks</b> that match your vibe.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# ------- SMALL CSS HELPER -------------------------------------------------
st.markdown(
    """
    <style>
    .artist-card{
        background:#121212;
        padding:0.5rem 2rem 1.5rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Input zone --------------------------------------------------------
st.markdown('<div class="artist-card">', unsafe_allow_html=True)

st.session_state.raw = st.text_area(
    "Pitch your mood :",
    value=st.session_state.raw or "",
    height=100,
    placeholder="I'm going on vacation to Italy with my best friend…",
)

# ---------- STEP 1 : Enrich ---------------------------------------------------
if st.session_state.enriched is None:

    if st.button("Enrich my prompt", use_container_width=True):

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

# ------------------------------------------------------------------
vibe_area = st.empty()

# ---------- STEP 2 : show enriched + actions ----------------------------------
if st.session_state.enriched:

    with vibe_area.container():
        st.subheader("🎼 Your vibe")
        st.write(st.session_state.enriched)

        col_a, col_b = st.columns(2)

        # -- Regenerate ------------------------------------------------------------
        with col_a:
            if st.button("🔁 Regenerate", use_container_width=True):
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
        disabled = (not st.session_state.enriched or st.session_state.loading_playlist)

        with col_b:
            if st.button("🚀 Get playlist", disabled=disabled, use_container_width=True):
                st.session_state.loading_playlist = True
                with st.spinner("Generating your playlist… ⏳"):
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

st.markdown("</div>", unsafe_allow_html=True)


# ----------  Séparateur  -----------------------------------------
st.markdown(
    "<hr style='border:none;border-top:1px solid #333;margin-top:1.5rem;'>",
    unsafe_allow_html=True,
)

# ----------  Toggle avec capture d'écran --------------------------------------
with st.expander("👀 Under the hood"):
    st.image(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'media/feature_2.png'), caption="Methodology feature 2", use_container_width=True)
