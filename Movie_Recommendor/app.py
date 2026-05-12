import streamlit as st

import gdown
import os

if not os.path.exists('similarity.pkl'):
    url = 'https://drive.google.com/file/d/196lfVcfpm4e9XEuISwOV9XH_pzzobZon/view?usp=sharing'
    gdown.download(url, 'similarity.pkl', quiet=False)

st.set_page_config(page_title="Movie Recommender", layout="wide")

pg = st.navigation([
        st.Page("pages/home.py", title="🎬 Home"),
        st.Page("pages/analysis.py", title="📊 Analysis")
])
pg.run()
