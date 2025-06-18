"""
spotify_api.py
──────────────
Centralise tous les appels Spotipy utilisés dans l’app.
"""

from spotipy import Spotify
from utils import get_spotify_client
import streamlit as st
import requests

# --- 1) New releases ------------------------------------------------------

def get_new_releases(country: str = "FR", n: int = 20):
    sp = get_spotify_client()

    try:
        new_albums = sp.new_releases(country=country, limit=n)["albums"]["items"]
    except Exception:
        new_albums = []

    return new_albums

# --- 2) Popular artists (fallback « Top 50 ») -----------------------------

def get_top_10(n: int = 10):
    # Enter Spotify API credentials
    client_id = st.secrets.get('spotify_client_id')
    client_secret = st.secrets.get('spotify_client_secret')

    # Get access token from the Spotify API
    response = requests.post('https://accounts.spotify.com/api/token', data={'grant_type': 'client_credentials'}, auth=(client_id, client_secret))
    access_token = response.json()['access_token']

    # Set up the headers for the HTTP GET request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # Send the HTTP GET request to the Spotify API for the top tracks
    response = requests.get('https://api.spotify.com/v1/playlists/6jdTMw4K4W55JdRzzrxgei/tracks?limit=10', headers=headers)
    top_tracks = response.json()['items']

    return top_tracks
