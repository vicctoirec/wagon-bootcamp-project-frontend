import requests
import streamlit as st
import streamlit.components.v1 as components
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_base_uri():
    base_uri = st.secrets.get('local_api_url', '')
    if not base_uri:
        st.error("API base URL ('local_api_url') not found in secrets!")
        return ""
    # Ensure trailing slash
    return base_uri if base_uri.endswith('/') else base_uri + '/'

def get_urls():
    base_uri = get_base_uri()
    return {
        'dummy_url': base_uri + 'predict',
        'themes_url': base_uri + 'predict-artist-themes',
        'artist_url' : base_uri + 'artists',
        'similar_artist_url' : base_uri + 'similar-songs/artists',
        'songs_by_artist_url' : base_uri + 'similar-songs/songs-by-artist',
        'enriched_url' : base_uri + 'enrich_prompt',
        'mood_url': base_uri + 'predict-mood-songs',
        'song_url': base_uri + 'predict-similar-songs',
        'lyrics_url': base_uri + 'explain-similar-lyrics'
    }


@st.cache_resource(show_spinner=False)
def get_spotify_client():
    client_id = st.secrets.get('spotify_client_id')
    client_secret = st.secrets.get('spotify_client_secret')
    if not client_id or not client_secret:
        st.error("Spotify client ID/secret not found in secrets!")
        return None
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_request(url, params=None):
    if not url:
        st.error("API URL is empty!")
        return None
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API request failed: {e}")
        return None

def display_themes(response):
    st.markdown("Check out these themes 🎵 ")
    themes = response['prediction']
    themes_md = "".join(themes)
    st.markdown(themes_md)

def display_songs(response):
    st.markdown("**Check out these tunes !🎵**")
    for song in response['prediction']:
        st.badge(f"{song[1]} - {song[0]}", color="green")


def display_matching_songs(songs):
    st.markdown("**Check out these tunes ! 🎵**")
    for item in songs:
        artist = item.get("artist", "")
        title  = item.get("track_title_clean", "")
        st.badge(f"{artist} — {title}", color="green")


def spotify_player(songs, cols_per_row: int = 3):
    """
    Affiche des players Spotify.

    Parameters
    ----------
    songs : list[tuple] | list[dict]
        •  [(artist, title), …]
        •  ou  [{"artist": …, "track_title_clean": …}, …]
        °  ou  [[artist, title], ...]
    cols_per_row : int
        Nombre de players par ligne (par défaut = 3).
    """
    sp = get_spotify_client()
    if not sp or not songs:
        return

    # ---------- normalisation (dicts → tuples) ------------------------------
    if isinstance(songs[0], dict):
        songs = [(s["artist"], s["track_title_clean"]) for s in songs]


    # ---------- récupération des track-ids ----------------------------------
    track_ids = []
    for artist, title in songs:
        query   = f"artist:{artist} track:{title}"
        items   = sp.search(q=query, type="track", limit=1)["tracks"]["items"]
        if items:
            track_ids.append(items[0]["id"])
        else:
            st.warning(f"Not found on Spotify: {artist} — {title}")

    # ---------- affichage par lignes de `cols_per_row` ----------------------
    for start in range(0, len(track_ids), cols_per_row):
        row_ids = track_ids[start:start + cols_per_row]
        cols    = st.columns(cols_per_row)
        for col, tid in zip(cols, row_ids):
            html = (
                f'<iframe src="https://open.spotify.com/embed/track/{tid}" '
                f'width="100%" height="80" frameborder="0" '
                f'allow="autoplay; clipboard-write; encrypted-media; picture-in-picture"></iframe>'
            )
            with col:
                components.html(html, height=100)
