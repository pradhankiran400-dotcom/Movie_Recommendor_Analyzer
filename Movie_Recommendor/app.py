import streamlit as st
import gdown
import os

# Always use absolute path for download
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
similarity_path = os.path.join(BASE_DIR, 'similarity.pkl')

if not os.path.exists(similarity_path):
    url = 'https://drive.google.com/uc?id=196lfVcfpm4e9XEuISwOV9XH_pzzobZon'
    gdown.download(url, similarity_path, quiet=False, fuzzy=True)

if os.path.exists(similarity_path):
    st.sidebar.success(f"✅ similarity.pkl loaded ({os.path.getsize(similarity_path) // 1024 // 1024} MB)")
else:
    st.sidebar.error("❌ similarity.pkl NOT found — download failed!")

st.set_page_config(page_title="Movie Recommender", layout="wide")
pg = st.navigation([
    st.Page("pages/home.py", title="🎬 Home"),
    st.Page("pages/analysis.py", title="📊 Analysis")
])
pg.run()
