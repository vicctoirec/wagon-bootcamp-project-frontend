import os
import streamlit as st
import requests


# Page config
st.set_page_config(
    page_title="AI Spotify Lyrics", # => Quick reference - Streamlit
    page_icon="🐍",
    layout="centered", # wide
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

# Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'
DUMMY_URL= BASE_URI + 'predict'
THEMES_URL = BASE_URI + 'predict-artist-themes'
MOOD_URL = BASE_URI + 'predict-mood-songs'
SONG_URL = BASE_URI + 'predict-similar-songs'


# Functions
def get_request(url, input, callback):
    try:
        params = {"input":input}
        response = requests.get(url, params)
        print(response)
        callback(response.json())
    except Exception as e:
        print(str(e))

def display_themes(response):
    st.markdown("**Here are the main themes !**")
    for theme in response['prediction']:
        st.badge(f"{theme}", color="red")

def display_songs(response):
    st.markdown("**Check out these tunes !**")
    for song in response['prediction']:
        st.badge(f"{song[0]} {song[1]}", color="green")


# Display API URL
st.text(f"API used: {DUMMY_URL}")


# Header
st.markdown("""
    # AI Spotify Lyrics

    - Get top themes by artists
    - Get recommended songs based on your mood
    - Get recommended songs based on a song
""")


# Return themes for an artist
st.header("Discover your artist")
artist = st.text_input("Search an artist", placeholder="Johnny Cash")
if st.button("Find themes", key="artist-btn"):
    get_request(THEMES_URL, artist, display_themes)


# Return songs from a mood
st.header("Find songs matching your mood")
mood = st.text_area("Pitch your mood",
                      placeholder="I'm going on vacation to Italy with my best friend. We plan to surf and talk about life/love... We love burning off energy in the evening by dancing.")
if st.button("Find songs", key="mood-btn"):
    get_request(MOOD_URL, mood, display_songs)


# Return songs from a song
st.header("Find songs matching your song")
song = st.text_input("Search a song", placeholder="Smoke Two Joints")
if st.button("Find songs", key="song-btn"):
    get_request(SONG_URL, song, display_songs)



# TODO: [OPTIONAL] maybe you can add some other pages?
#   - some statistical data you collected in graphs
#   - description of your product
#   - a 'Who are we?'-page
