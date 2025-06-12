import requests
import streamlit as st
import streamlit.components.v1 as components
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_base_uri():
    base_uri = st.secrets.get('cloud_api_url', '')
    if not base_uri:
        st.error("API base URL ('cloud_api_url') not found in secrets!")
        return ""
    # Ensure trailing slash
    return base_uri if base_uri.endswith('/') else base_uri + '/'

def get_urls():
    base_uri = get_base_uri()
    return {
        'dummy_url': base_uri + 'predict',
        'themes_url': base_uri + 'predict-artist-themes',
        'mood_url': base_uri + 'predict-mood-songs',
        'song_url': base_uri + 'predict-similar-songs',
    }

def get_spotify_client():
    client_id = st.secrets.get('spotify_client_id')
    client_secret = st.secrets.get('spotify_client_secret')
    if not client_id or not client_secret:
        st.error("Spotify client ID/secret not found in secrets!")
        return None
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_request(url, input_text):
    if not url:
        st.error("API URL is empty!")
        return None
    try:
        params = {"input": input_text}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API request failed: {e}")
        return None

def display_themes(response):
    st.markdown("**Check out these themes 🎵 🎵 🎵 **")
    themes = response['prediction']
    themes_md = "".join(themes)
    st.markdown(themes_md)

def display_songs(response):
    st.markdown("**Check out these tunes ! 🎵 🎵 🎵 **")
    for song in response['prediction']:
        st.badge(f"{song[1]} - {song[0]}", color="green")


def spotify_player(songs):
    sp = get_spotify_client()
    if not sp:
        return
    track_ids = []

    for artist, title in songs:
        query = f"artist:{artist} track:{title}"
        results = sp.search(q=query, type="track", limit=1)
        items = results['tracks']['items']
        if items:
            track_ids.append(items[0]['id'])
        else:
            st.warning(f"Song not found on Spotify: {artist} - {title}")

    # Create columns equal to number of tracks
    cols = st.columns(len(track_ids))

    # Embed each track in its own column
    for col, tid in zip(cols, track_ids):
        html_code = f"""
            <iframe src="https://open.spotify.com/embed/track/{tid}" width="300" height="80" frameborder="0"
                allowtransparency="true" allow="encrypted-media"></iframe>
        """
        with col:
            components.html(html_code, height=100)
