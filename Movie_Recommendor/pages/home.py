import streamlit as st
import pickle
import pandas as pd
import requests
import base64

def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                        url("data:image/jpg;base64,{img_data}");
            background-size: cover;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("image.jpg")

movies     = pd.DataFrame(pickle.load(open('movies.pkl', 'rb')))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b29bc66ed87b5d4259606b0810101c03"
    try:
        data = requests.get(url, timeout=10).json()
        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    except:
        pass
    return "https://placehold.co/500x750?text=No+Poster"

def recommend(movie):
    idx     = movies[movies["title"] == movie].index[0]
    scores  = sorted(enumerate(similarity[idx]), reverse=True, key=lambda x: x[1])[1:8]
    names   = [movies.iloc[i].title                for i, _ in scores]
    posters = [fetch_poster(movies.iloc[i].movie_id) for i, _ in scores]
    return names, posters

st.title("🎬 Movie Recommender")

selected = st.selectbox("Pick a movie:", movies["title"].values)

if st.button("Recommend"):
    with st.spinner("Finding movies…"):
        names, posters = recommend(selected)

    st.subheader("You might also like:")
    for col, name, poster in zip(st.columns(7), names, posters):
        with col:
            st.image(poster)
            st.caption(name)