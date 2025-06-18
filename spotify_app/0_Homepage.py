"""
🎧  Spotify-style landing page
────────────────────────────
Affiche une “home” dynamique (trending tracks / new releases / popular artists)
et rappelle les trois features de l’app.
"""

import streamlit as st
import spotipy
import sys
import textwrap
from spotify_style import apply           # thème global dark spotify
from spotify_api import get_new_releases, get_top_10
from utils import get_spotify_client
sp = get_spotify_client()

# -- THEME ---------------------------------------------------------------------
SPOTIFY_GREEN = "#1DB954"
FONT_URL      = "https://fonts.googleapis.com/css2?family=Circular+Std:wght@400;700&display=swap"

st.set_page_config(page_title="AI Spotify Lyrics", page_icon="🎧", layout="wide", initial_sidebar_state="collapsed")
apply()

st.markdown(
    f"""
    <style>
    @import url('{FONT_URL}');

    html, body, [class*="css"]  {{
        font-family: 'Circular Std', sans-serif !important;
    }}

    /* --- HERO ------------------------------------------------------------ */
    .hero {{
        background:linear-gradient(135deg,#1DB954 0%,#0d1 55%,#000 100%);
        padding:2rem 3rem 2rem;
        border-radius:1rem;
        box-shadow:0 8px 24px rgba(0,0,0,.4);
    }}
    .hero h1 {{font-size:2.3rem;line-height:1.15;margin:0 0 .5rem}}
    .hero p  {{margin:0 0 1.5rem;opacity:.85}}
    .hero a  {{color:#fff !important; text-decoration:none;}}
    .hero a:hover{{text-decoration:underline;}}

    /* --- CARDS ----------------------------------------------------------- */
        .card-wrap {{
            display:grid;
            grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
            gap:28px;
            margin-top:1.5rem;
        }}
        .card {{
            background:#181818;
            padding:1rem;
            border-radius:.75rem;
            transition:transform .15s;
            box-shadow:0 0 10px rgba(0,0,0,.4);
        }}
        .card:hover {{ transform:scale(1.06); }}
        .card img{{border-radius:.5rem;width:100%;height:auto}}
        .card-title{{margin:.6rem 0 0;font-weight:700;font-size:0.95rem}}
        .card-sub  {{opacity:.8;font-size:.8rem}}

    /* --- BOUTON ---------------------------------------------------------- */
    .cta {{
        background:{SPOTIFY_GREEN};
        color:#fff;padding:.75rem 1.8rem;
        border:none;border-radius:9999px;font-weight:700;
        cursor:pointer;font-size:1rem;margin-top:1.2rem;
    }}
    .cta:hover{{background:#1ED760}}
    </style>
    """,
    unsafe_allow_html=True,
)

# HERO  ------------------------------------------------------------------------
with st.container():
    st.markdown(
        """
        <div class="hero">
            <h1>Feel the music.<br/>Read the lyrics.</h1>
            <p>Three AI-powered features to help you fine-tune your musics choices thanks to lyrics
            – all inside a Spotify-like experience.</p>
            <a href="#features" class="cta">Jump in features description ↓</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div id='discover'></div>", unsafe_allow_html=True)

# CHARGEMENT DONNÉES  ----------------------------------------------------------
@st.cache_data(ttl=3600)
def _fetch():
    return get_new_releases(), get_top_10()  # new_albums, top_tracks

try:
    new_albums, top_tracks = _fetch()
except Exception as err:
    st.error(f"Could not reach Spotify API ({err})."); st.stop()


#  Affichage vignettes ---------------------------------------------------------
def card_grid(
        items, *, cover, title, subtitle,
        n_cols: int = 6, img_h: int = 160
    ):
    rows = [items[i:i+n_cols] for i in range(0, len(items), n_cols)]
    for row in rows:
        cols = st.columns(n_cols, gap="small")
        for i in range(n_cols):
            with cols[i]:
                if i < len(row):
                    it = row[i]
                    st.image(cover(it), use_container_width=True,
                             clamp=True, output_format="JPEG", caption=None)
                    st.markdown(
                        f"<b>{title(it)}</b><br>"
                        f"<span style='font-size:.8rem;opacity:.7'>"
                        f"{subtitle(it)}</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.empty()



# SECTIONS  --------------------------------------------------------------------
st.subheader("🔥 Trending tracks")
card_grid(
    top_tracks[:10],
    cover   = lambda it: it['track']['album']['images'][0]['url'],
    title  = lambda it: textwrap.shorten(it['track']['name'], 22),
    subtitle = lambda it: ', '.join(it['track']['artists'][i]['name'] for i in range(len(it['track']['artists']))),
)


st.subheader("🆕 New releases")
card_grid(
    new_albums[:10],
    cover   = lambda it: it["images"][0]["url"],
    title   = lambda it: textwrap.shorten(it["name"], 22),
    subtitle= lambda it: ", ".join(a["name"] for a in it["artists"]),
)

# FEATURES ---------------------------------------------------------------------
st.markdown('<div id="features"></div>', unsafe_allow_html=True)

fcol1, fcol2, fcol3 = st.columns(3)

with fcol1:
    with st.expander("🎤  Theme explorer (by artist)"):
        st.markdown(
            """
        - **Enter your favourite artist's name**
        - We analyse *all* their lyrics
        - You get a neat write-up of their 3 main themes
            """
        )

with fcol2:
    with st.expander("😊  Mood-mix playlist"):
        st.markdown(
            """
        - **Describe today’s mood** in a few words
        - Receive a brief, personalized mood description
        - Enjoy a curated 10-songs playlist that perfectly match your mood
            """
        )

with fcol3:
    with st.expander("🎵  Similar-song finder"):
        st.markdown(
            """
        - **Pick your favorite track & artist**
        - We hunt down songs whose *lyrics* match your preferred beats and lyrics
        - Enjoy smooth playback right inside the app
        - Click *Explain* to see why the matches work
            """
        )
