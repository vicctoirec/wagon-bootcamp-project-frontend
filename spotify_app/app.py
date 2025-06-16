import streamlit as st

st.set_page_config(page_title="AI Spotify Lyrics", page_icon="🐍🎵", layout="wide")

st.sidebar.image(
    "https://plus.unsplash.com/premium_photo-1682125853703-896a05629709?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    caption="Vibes for your music journey",
    use_container_width=True
)

st.title("Welcome to AI Spotify Lyrics")

st.markdown("""
We've built 3 features to help you finetume your music choices thanks to lyrics

Use the built-in page switcher in the sidebar to navigate between pages.
""")

# Creating basic columns for titles
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🎶 Feature 1: Discover Top Themes in Your Favorite Artist's Lyrics**")

with col2:
    st.markdown("**😊 Feature 2: Get Song Recommendations Based on Your Mood**")

with col3:
    st.markdown("**🔥 Feature 3: Find Songs Similar to Your Favorite Track**")

# Creating expanders in a new row of columns so they align horizontally
exp_col1, exp_col2, exp_col3 = st.columns(3)

with exp_col1:
    with st.expander("More info"):
        st.markdown("""
        - 🎤 **Enter your favorite artist’s name**
        - 🔍 **Uncover the main themes and stories behind their lyrics**
        - ▶️ **Listen to your artist’s top songs right here in the app**
        """)

with exp_col2:
    with st.expander("More info"):
        st.markdown("""
        - 📝 **Tell us how you’re feeling today**
        - ✍️ **Receive a brief, personalized mood description**
        - 🎧 **Enjoy a curated 5-song playlist that perfectly matches your vibe**
        - ▶️ **Play the playlist seamlessly within the app**
        """)

with exp_col3:
    with st.expander("More info"):
        st.markdown("""
        - 🎵 **Input your favorite song and artist**
        - 🎶 **Discover a 5-song playlist tailored to your preferred beats and lyrics**
        - ▶️ **Enjoy smooth playback right inside the app**
        """)
