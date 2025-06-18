# spotify_app/pages/0_Home.py
"""
🎧  Spotify-style landing page
────────────────────────────
Affiche la “home” dynamique (trending tracks / new releases / popular artists)
et rappelle les trois features de l’app.
"""

import streamlit as st
import spotipy
import sys
import textwrap
from spotify_style import apply           # thème global dark spotify
from spotify_api import get_home_sections

# -- 1️⃣  THEME ----------------------------------------------------------------
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
        height:360px;
        background:linear-gradient(135deg, {SPOTIFY_GREEN} 0%, #121212 55%);
        border-radius:0.75rem;
        padding:3.5rem 4rem;
        display:flex;flex-direction:column;justify-content:center;
        box-shadow:0 0 24px rgba(0,0,0,.6);
        color:#fff;
    }}
    .hero h1 {{font-size:3rem;margin:0 0 .5rem 0}}
    .hero p  {{opacity:.85;font-size:1.15rem;margin:0}}

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

# 2️⃣  HERO  -------------------------------------------------------------------
with st.container():
    st.markdown(
        """
        <div class="hero">
            <h1>Feel the music.<br/>Read the lyrics.</h1>
            <p>Three AI-powered features to help you fine-tune your musics choices thanks to lyrics
            – all inside a Spotify-like experience.</p>
            <a href="#discover" class="cta">Jump in ↓</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div id='discover'></div>", unsafe_allow_html=True)

# 3️⃣  CHARGEMENT DONNÉES  -----------------------------------------------------
@st.cache_data(ttl=3600)
def _fetch():
    return get_home_sections()    # trending, new_albums, popular_artists

try:
    trending, new_albums, popular_artists = _fetch()
except Exception as err:
    st.error(f"Could not reach Spotify API ({err})."); st.stop()

#  helper affichage vignettes ----------------------------------------
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
                    st.image(cover(it), use_column_width=True,
                             clamp=True, output_format="JPEG", caption=None)
                    st.markdown(
                        f"<b>{title(it)}</b><br>"
                        f"<span style='font-size:.8rem;opacity:.7'>"
                        f"{subtitle(it)}</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.empty()

# 5️⃣  SECTIONS  ---------------------------------------------------------------
st.subheader("🔥 Trending tracks")
card_grid(
    trending[:10],
    cover   = lambda it: it["track"]["album"]["images"][0]["url"],
    title   = lambda it: textwrap.shorten(it["track"]["name"], 22),
    sub     = lambda it: it["track"]["artists"][0]["name"],
)

st.subheader("🆕 New releases")
card_grid(
    new_albums[:10],
    cover   = lambda it: it["images"][0]["url"],
    title   = lambda it: textwrap.shorten(it["name"], 22),
    sub     = lambda it: ", ".join(a["name"] for a in it["artists"]),
)

st.subheader("🎤 Popular artists")
card_grid(
    popular_artists[:10],
    cover   = lambda it: it["album"]["images"][0]["url"],
    title   = lambda it: it["name"],
    sub     = lambda it: it["artists"][0]["name"],
)
