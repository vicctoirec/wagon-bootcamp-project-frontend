import os
import requests

import streamlit as st
import streamlit.components.v1 as components

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



# Page config
st.set_page_config(
    page_title="AI Spotify Lyrics", # => Quick reference - Streamlit
    page_icon="🐍",
    layout="wide", # wide
    initial_sidebar_state="auto") # collapsed


# Define the base URI of the API
#   - Potential sources are in `.streamlit/secrets.toml` or in the Secrets section
#     on Streamlit Cloud
#   - The source selected is based on the shell variable passend when launching streamlit
#     (shortcuts are included in Makefile). By default it takes the cloud API url
if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['cloud_api_url']


# --- Setup Spotify API ---
client_id = st.secrets['spotify_client_id']
client_secret = st.secrets['spotify_client_secret']
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# --- URLs ---
# Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'
DUMMY_URL= BASE_URI + 'predict'
THEMES_URL = BASE_URI + 'predict-artist-themes'
MOOD_URL = BASE_URI + 'predict-mood-songs'
SONG_URL = BASE_URI + 'predict-similar-songs'


# --- Functions ---
def get_request(url, input, callback):
    try:
        params = {"input":input}
        response = requests.get(url, params)
        callback(response.json())
        return response.json()
    except Exception as e:
        print(str(e))

def display_themes(response):
    st.markdown("**Here are the main themes !**")
    for theme in response['prediction']:
        st.badge(f"{theme}", color="red")

def display_songs(response):
    st.markdown("**Check out these tunes !**")
    for song in response['prediction']:
        st.badge(f"{song[1]} - {song[0]}", color="green")

def spotify_player(songs):
    track_ids = []

    # Get track ids
    for artist, title in songs:
        query = f"artist:{artist} track:{title}"
        results = sp.search(q=query, type="track", limit=1)
        items = results['tracks']['items']
        if items:
            track_ids.append(items[0]['id'])
        else:
            st.write(f"Song not found on Spotify: {artist} - {title}")

    # Embed all tracks
    for tid in track_ids:
        html_code = f"""
        <iframe src="https://open.spotify.com/embed/track/{tid}" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """
        components.html(html_code, height=100)


# --- Initialize session state ---
for key in ["artist-btn_clicked", "mood-btn_clicked", "song-btn_clicked"]:
    if key not in st.session_state:
        st.session_state[key] = False

for key in ["artist_themes", "mood_songs", "song_songs"]:
    if key not in st.session_state:
        st.session_state[key] = None


# --- UI ---
# Display API URL
st.text(f"API used: {DUMMY_URL}")

# Header
st.markdown("""
    # AI Spotify Lyrics

    - Get top themes by artists
    - Get recommended songs based on your mood
    - Get recommended songs based on a song
""")

# Define container
c = st.container()

col1, col2, col3 = c.columns(3)

with col1:
    st.header("Discover your artist")
    artist = st.text_input("Search an artist", placeholder="Johnny Cash")

    if st.button("Find themes", key="artist-btn"):
        #Record that button was clicked
        st.session_state["artist-btn_clicked"] = True

        # Fetch and save output in session_state
        result = get_request(THEMES_URL, artist, display_themes)
        st.session_state["artist_themes"] = result

    # Display persisted output if available
    if st.session_state["artist_themes"]:
        display_themes(st.session_state["artist_themes"])


with col2:
    st.header("Find songs matching your mood")
    mood = st.text_area("Pitch your mood",
                        placeholder="I'm going on vacation to Italy with my best friend...")

    if st.button("Find songs", key="mood-btn"):
        #Record that button was clicked
        st.session_state["mood-btn_clicked"] = True

        # Fetch and save output in session_state
        result = get_request(MOOD_URL, mood, display_songs)
        st.session_state["mood_songs"] = result['prediction']

    # Display persisted output if available
    if st.session_state["mood_songs"]:
        spotify_player(st.session_state["mood_songs"])


with col3:
    st.header("Find songs matching your song")
    song = st.text_input("Search a song", placeholder="Smoke Two Joints")

    if st.button("Find songs", key="song-btn"):
        #Record that button was clicked
        st.session_state["song-btn_clicked"] = True

        # Fetch and save output in session_state
        result = get_request(SONG_URL, song, display_songs)
        st.session_state["song_songs"] = result['prediction']

    # Display persisted output if available
    if st.session_state["song_songs"]:
        spotify_player(st.session_state["song_songs"])



# TODO: [OPTIONAL] maybe you can add some other pages?
#   - some statistical data you collected in graphs
#   - description of your product
#   - a 'Who are we?'-page
