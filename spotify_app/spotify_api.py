# spotify_app/spotify_api.py
import streamlit as st, spotipy
from spotipy.oauth2 import SpotifyClientCredentials

@st.cache_resource(show_spinner=False)
def sp():
    cid     = st.secrets.get("spotify_client_id")
    secret  = st.secrets.get("spotify_client_secret")
    if not cid or not secret:
        st.warning("Spotify keys missing in secrets.toml")
        return None
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=cid, client_secret=secret))

# 1) Trending : on récupère la playlist “Global Top 50” via son ID
TREND_PLAY_ID = "37i9dQZEVXbMDoHDwVN2tF"

def get_trending(limit=10, market="FR"):
    sp = sp()
    if sp is None:
        return []

    items = sp.playlist_items(
        TREND_PLAY_ID,
        limit=limit,
        market=market,
        additional_types=("track",)
    )["items"]

    return items
