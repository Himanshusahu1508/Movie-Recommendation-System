import streamlit as st
import pickle
import pandas as pd
import requests

import os
if not os.path.exists("similarity.pkl"):
    import gdown
    url = "https://drive.google.com/uc?id=1mTuiHEDY7yAcrdIViXK0eWjxpfSRgDyW"
    gdown.download(url, "similarity.pkl", quiet=False)


# OMDb API Key
api_key = "d20dabfc"

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch poster using OMDb API
def fetch_poster(movie_id):
    movie_name = movies.iloc[movie_id].title
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_name}"
    response = requests.get(url)
    data = response.json()
    return data.get('Poster', 'https://via.placeholder.com/300x450?text=No+Image')

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []
    for i in movies_list:
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(i[0]))
    return recommended_titles, recommended_posters

# Streamlit page config
st.set_page_config(page_title="Movie Recommender", layout="centered")

# CSS styling
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #FAFAFA;
    }
    .main {
        background-color: #0e1117;
        color: white;
    }
    .title {
        font-size: 45px;
        font-weight: 700;
        color: #f39c12;
        margin-bottom: 10px;
        text-align: center;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #bbbbbb;
        margin-bottom: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# Title & subtitle
st.markdown("""
    <div class="title">🍿🎬 <span style='color:#f39c12;'>Movie Recommender</span></div>
""", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find similar movies based on your favorites</div>', unsafe_allow_html=True)

# Movie input
selected_movie_name = st.selectbox('Choose a movie you like:', movies['title'].values)

# Recommend button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    st.subheader("🎥 Top Recommendations:")

    # Display recommendations in columns
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.caption(names[idx])
