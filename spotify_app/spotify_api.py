"""
spotify_api.py
──────────────
Centralise tous les appels Spotipy utilisés dans l’app.
"""

from spotipy import Spotify
from utils import get_spotify_client
import streamlit as st

# ------------------------------------------------------------------
# 1.  CONNEXION
# ------------------------------------------------------------------
sp = get_spotify_client()

# ------------------------------------------------------------------
# 2.  HOME SECTIONS
#     → renvoie 3 listes : trending tracks, new albums, popular artists
# ------------------------------------------------------------------
def get_home_sections(country: str = "FR", n: int = 20):
    """
    Returns (trending_tracks, new_albums, popular_artists)

    • trending_tracks   : sp.playlist_items d’une playlist « Top Hits »
    • new_albums        : sp.new_releases
    • popular_artists   : on triche en prenant les titres d’un « Top 50 »
    """
    if sp is None:
        return [], [], []

    # --- 1) Trending playlist -------------------------------------------------
    try:
        pl = sp.featured_playlists(country=country, limit=1)["playlists"]["items"][0]
        trending = sp.playlist_items(pl["id"], limit=n)["items"]
        if not trending:                                             # ← fallback
            trending = sp.playlist_items("37i9dQZEVXbMDoHDwVN2tF",   # Top 50
                                           limit=n)["items"]
    except Exception:
        trending = []

    # --- 2) New releases ------------------------------------------------------
    try:
        new_albums = sp.new_releases(country=country, limit=n)["albums"]["items"]
    except Exception:
        new_albums = []

    # --- 3) Popular artists (fallback « Top 50 ») -----------------------------
    try:
        top50 = sp.search(q="tag:hipster", type="track", limit=n)["tracks"]["items"]
        popular_artists = top50
    except Exception:
        popular_artists = []

    return trending, new_albums, popular_artists
