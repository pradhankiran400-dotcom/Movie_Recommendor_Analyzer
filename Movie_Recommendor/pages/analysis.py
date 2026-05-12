import streamlit as st
import pickle
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
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

set_background("analysis.jpg")

df = pd.DataFrame(pickle.load(open('df_m.pkl', 'rb')))
df = df.loc[:, ~df.columns.duplicated()]
df = df.reset_index(drop=True)
df['profit'] = df['revenue'] - df['budget']

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b29bc66ed87b5d4259606b0810101c03"
    try:
        data = requests.get(url).json()
        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    except:
        pass
    return "https://placehold.co/500x750?text=No+Poster"

def plot_rating(rating):
    fig, ax = plt.subplots(figsize=(6, 1))
    ax.barh("Rating", 10, color="lightgrey")
    ax.barh("Rating", rating, color="red")
    ax.set_xlim(0, 10)
    plt.title(f"Rating: {rating}/10")
    return fig

def plot_budget_revenue(budget, revenue):
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = ["budget", "revenue"]
    values = [budget, revenue]
    sns.barplot(x=labels, y=values, palette=["orange", "green"], ax=ax)
    plt.title("Budget vs Revenue")
    plt.ylabel("Amount (USD)")
    return fig

st.title("📊 Movie Analysis")

selected = st.selectbox("Select a Movie", df["title"].values)

if st.button("Analyse"):
    movie = df[df["title"] == selected].iloc[0]
    poster = fetch_poster(movie["movie_id"])

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(poster, width=250)

    with col2:
        st.title(movie["title"])
        st.write(f"⭐ Rating    : {movie['rating']} / 10")
        st.write(f"⏱️ Runtime   : {movie['runtime']} mins")
        st.write(f"💰 Budget    : ${movie['budget']:,}")
        st.write(f"🎟️ Revenue   : ${movie['revenue']:,}")
        st.write(f"💵 Profit    : ${movie['profit']:,}")
        st.write(f"🎭 Genres    : {', '.join(movie['genres']) if isinstance(movie['genres'], list) else movie['genres']}")
        st.write(f"🎬 Actors    : {', '.join(movie['actors']) if isinstance(movie['actors'], list) else movie['actors']}")

    st.divider()

    st.subheader("📖 Overview")
    st.write(movie["overview"])

    st.divider()

    st.subheader("📊 Visual Analysis")

    g1, g2 = st.columns(2)
    with g1:
        st.pyplot(plot_rating(movie["rating"]))
    with g2:
        st.pyplot(plot_budget_revenue(movie["budget"], movie["revenue"]))

    profit = movie["profit"]
    rating = movie["rating"]

    if profit > 0 and rating >= 7:
        st.success(f"✅ {selected} — Hit Movie! Great Rating & Profitable!")
    elif profit > 0 and rating < 7:
        st.info(f"ℹ️ {selected} — Profitable but Average Rating!")
    elif profit < 0 and rating >= 7:
        st.warning(f"⚠️ {selected} — Good Rating but Box Office Flop!")
    else:
        st.error(f"❌ {selected} — Flop Movie!")
