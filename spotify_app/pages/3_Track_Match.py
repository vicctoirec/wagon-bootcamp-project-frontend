# --------------------------PARAMS & IMPORT-------------------------------------
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils import get_request, display_songs, spotify_player, get_urls
from spotify_style import apply as apply_style, hero

urls = get_urls()
SONG_URL = urls.get('song_url', '') # Endpoint qui retourne les chansons similaires
LYRICS_URL = urls.get('lyrics_url', '') # Endpoint qui explique en quoi les lyrics des chansons les plus proches sont similaires
ARTISTS_URL = urls.get('similar_artist_url', '') # Get a list of available artists
ARTIST_SONG_URL = urls.get('songs_by_artist_url', '') # Get a list of available songs by artist input
# ------------------------------------------------------------------------------

# ----------- Streamlit config & style------------------------------------------
st.set_page_config(page_title="Find Similar Songs", page_icon="🎵", layout="wide")
apply_style()
hero(
    title     = "Discover songs with lyrics just like yours 🫵",
    subtitle  = "Pick a track&nbsp;→&nbsp;we’ll hunt down songs whose <b>lyrics share the same vibe</b>.",
    btn_text  = None,
    link      = None,
)

# ---------- Caches ------------------------------------------------------------
@st.cache_data(ttl=3_600, show_spinner="Loading artist list…")
def fetch_artists():
    res = get_request(ARTISTS_URL)
    return sorted(res.get("results", []))

@st.cache_data(ttl=3_600, show_spinner=False)
def fetch_songs_by_artist(artist: str) -> list[str]:
    """Retourne la liste des titres pour un artiste (ou [] si échec)."""
    if not artist:
        return []
    res = get_request(ARTIST_SONG_URL, params={"input": artist})
    return sorted(res.get("results", []))

# ----------- Init state -------------------------------------------------------
for k in (
    "artist_choice", "song_choice",
    "song_songs",       # résultat de SONG_URL
    "lyrics_explain",   # résultat de LYRICS_URL
):
    st.session_state.setdefault(k, None)


st.divider()

st.markdown(
    """
    <style>
    .artist-card{
        background:#191414;
        padding:0.5rem 1.5rem 0.5rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------  Sélection ARTISTE ------------------------------------------------
st.markdown('<div class="artist-card">', unsafe_allow_html=True)

artist_list = fetch_artists()
if artist_list:
            placeholder  = "Search an artist"
            selection    = st.selectbox("🎧 Select an artist", [placeholder] + artist_list)

            st.session_state.artist_choice = None if selection == placeholder else selection

if "song_choice" in st.session_state:
            st.session_state.song_choice = None

else:           # fallback texte libre
            st.session_state.artist_choice = st.text_input(
                "🎤 Type an artist", placeholder="Johnny Cash"
            ).strip() or None

# ----------  Sélection CHANSON ------------------------------------------------

if st.session_state.artist_choice:
    song_options = fetch_songs_by_artist(st.session_state.artist_choice)

    if song_options :
        song_sel = st.selectbox(
            "🎵 Select a song",
            ["Search a song"] + song_options,
            index=0,
            key="song_choice_select",
        )
        st.session_state.song_choice = None if song_sel == "—" else song_sel

    else:
        st.session_state.song_choice = st.text_input(
        "🎵 Type a song", placeholder="Thriller"
    ).strip() or None

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

# ----------  Affichage lecteur Spotify de la chanson sélectionnée ------------
valid_song_selected = (
    st.session_state.artist_choice
    and st.session_state.song_choice
    and st.session_state.song_choice != "Search a song"
)

if valid_song_selected:
    spotify_player([{
        "artist": st.session_state.artist_choice,
        "track_title_clean":  st.session_state.song_choice
    }])

# ----------  Bouton « Find similar song » ------------------------------------
find_disabled = not (st.session_state.artist_choice and st.session_state.song_choice)
if st.button("🚀 Find similar songs", key='similar-btn', disabled=find_disabled, use_container_width=True):
    with st.spinner("Searching similar tracks…"):
        st.session_state.song_songs = None          # reset anciens résultats
        st.session_state.lyrics_explain = None

        res = get_request(
            SONG_URL,
            params={
                "input_song":   st.session_state.song_choice,
                "input_artist": st.session_state.artist_choice,
            },
        )
    if res and "prediction" in res:
        st.session_state.song_songs = res["prediction"]
    else:
        st.error("API error: could not retrieve similar songs.")

# ----------  Affichage playlist + bouton « Explain similarities » ------------
if st.session_state.song_songs:
    st.markdown("<hr style='border:none;border-top:1px solid #333;'>", unsafe_allow_html=True)
    display_songs({"prediction": st.session_state.song_songs})
    spotify_player(st.session_state.song_songs)

    # -- bouton explication ----------------------------------------------------
    explain_disabled = st.session_state.lyrics_explain is not None
    if st.button("💬 Explain similarities", disabled=explain_disabled, use_container_width=True):
        with st.spinner("Analysing lyrics…"):
            res = get_request(
                LYRICS_URL,
                params={
                    "input_song":   st.session_state.song_choice,
                    "input_artist": st.session_state.artist_choice,
                },
            )
        if res and "prediction" in res:
            st.session_state.lyrics_explain = res["prediction"]
        else:
            st.error("API error: could not retrieve explanation.")

# ----------  Affichage explications ------------------------------------------
if st.session_state.lyrics_explain:
    st.subheader("📝 Why are these tracks similar ?")
    st.markdown(st.session_state.lyrics_explain)

st.markdown("</div>", unsafe_allow_html=True)

# ----------  Séparateur  -----------------------------------------
st.markdown(
    "<hr style='border:none;border-top:1px solid #333;margin-top:1.5rem;'>",
    unsafe_allow_html=True,
)

# ----------  Toggle avec capture d'écran --------------------------------------
with st.expander("👀 Under the hood"):
    st.image(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'media/feature_3.png'), caption="Methodology feature 3", use_container_width=True)
