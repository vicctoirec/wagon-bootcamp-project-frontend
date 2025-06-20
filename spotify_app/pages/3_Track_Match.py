# --------------------------PARAMS & IMPORT-------------------------------------
import sys
import os
import base64
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

# # Convertir l'image en base64
# with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'media/qr_code.jpg'), "rb") as f:
#     img_data = f.read()
# img_base64 = base64.b64encode(img_data).decode()

# # Affichage centré dans la sidebar
# st.sidebar.markdown(
#     f"""
#     <div style="text-align: center;">
#         <img src="data:image/png;base64,{img_base64}" width="130"/>
#         <p style="margin-top: 0.5rem;">Try the app!</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

hero(
    title     = "Discover songs with lyrics just like yours 🫵",
    subtitle  = "Pick a track&nbsp;→&nbsp;we’ll hunt down songs whose <b>lyrics share the same vibe</b>.",
    btn_text  = None,
    link      = None,
)

for k in ("artist_themes", "artist_choice", "sm_artist_choice", "sm_song_choice", "sm_song_songs", "sm_lyrics_explain"):
    if k not in st.session_state:
        st.session_state.setdefault(k, None)

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

# ----------- Reset callbacks --------------------------------------------------
def reset_on_artist_change():
    st.session_state.sm_song_choice = None
    st.session_state.sm_song_songs = None
    st.session_state.sm_lyrics_explain = None

def reset_on_song_change():
    st.session_state.sm_song_songs = None
    st.session_state.sm_lyrics_explain = None

# ----------- UI ---------------------------------------------------------------
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
    index = artist_list.index(st.session_state.sm_artist_choice) if st.session_state.sm_artist_choice else None
    artist_sel  = st.selectbox("🎧  Select an artist",
                                artist_list,
                                placeholder=placeholder,
                                index = index,
                                on_change=reset_on_artist_change)

    st.session_state.sm_artist_choice = artist_sel

else:        # fallback texte libre
    st.session_state.sm_artist_choice = st.text_input(
        "🎤 Type an artist", placeholder="Johnny Cash"
    ).strip() or None

# ----------  Sélection CHANSON ------------------------------------------------

if st.session_state.sm_artist_choice:
    song_options = fetch_songs_by_artist(st.session_state.sm_artist_choice)
    index = song_options.index(st.session_state.sm_song_choice) if st.session_state.sm_song_choice else None
    if song_options :
        song_sel = st.selectbox(
            "🎵 Select a song",
            song_options,
            placeholder="Search a song",
            index=index,
            key="song_choice_select",
            on_change=reset_on_song_change
        )
        st.session_state.sm_song_choice = song_sel

    else:
        st.session_state.sm_song_choice = st.text_input(
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
    st.session_state.sm_artist_choice
    and st.session_state.sm_song_choice
)

if valid_song_selected:
    spotify_player([{
        "artist": st.session_state.sm_artist_choice,
        "track_title_clean":  st.session_state.sm_song_choice
    }])

# ----------  Bouton « Find similar song » ------------------------------------
find_disabled = not (st.session_state.sm_artist_choice and st.session_state.sm_song_choice)
if st.button("🚀 Find similar songs", key='similar-btn', disabled=find_disabled, use_container_width=True):
    with st.spinner("Searching similar tracks…"):
        st.session_state.sm_song_songs = None          # reset anciens résultats
        st.session_state.sm_lyrics_explain = None

        res = get_request(
            SONG_URL,
            params={
                "input_song":   st.session_state.sm_song_choice,
                "input_artist": st.session_state.sm_artist_choice,
            },
        )
    if res and "prediction" in res:
        st.session_state.sm_song_songs = res["prediction"]
    else:
        st.error("API error: could not retrieve similar songs.")

# ----------  Affichage playlist + bouton « Explain similarities » ------------
if st.session_state.sm_song_songs:
    st.markdown("<hr style='border:none;border-top:1px solid #333;'>", unsafe_allow_html=True)
    display_songs({"prediction": st.session_state.sm_song_songs})
    spotify_player(st.session_state.sm_song_songs)

    # -- bouton explication ----------------------------------------------------
    explain_disabled = st.session_state.sm_lyrics_explain is not None
    if st.button("💬 Explain similarities", disabled=explain_disabled, use_container_width=True):
        with st.spinner("Analysing lyrics…"):
            res = get_request(
                LYRICS_URL,
                params={
                    "input_song":   st.session_state.sm_song_choice,
                    "input_artist": st.session_state.sm_artist_choice,
                },
            )
        if res and "prediction" in res:
            st.session_state.sm_lyrics_explain = res["prediction"]
        else:
            st.error("API error: could not retrieve explanation.")

# ----------  Affichage explications ------------------------------------------
if st.session_state.sm_lyrics_explain:
    st.subheader("📝 Why are these tracks similar ?")
    st.markdown(st.session_state.sm_lyrics_explain)

st.markdown("</div>", unsafe_allow_html=True)

# ----------  Séparateur  -----------------------------------------
st.markdown(
    "<hr style='border:none;border-top:1px solid #333;margin-top:1.5rem;'>",
    unsafe_allow_html=True,
)

# ----------  Toggle avec capture d'écran --------------------------------------
with st.expander("👀 Under the hood"):
    st.image(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'media/feature_3.png'), caption="Methodology feature 3", use_container_width=True)
