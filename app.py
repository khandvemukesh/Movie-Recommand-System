# import streamlit as st
# import pickle as p
# import joblib as jl
# st.title("Movie Recommand System")

# with open("movies.pickle", 'rb') as movie:
#       movies=p.load(movie)

# similarities = jl.load("similarities.joblib")

# def recommand(name_movies):
#     movies_index = movies[movies['title'].str.lower() == name_movies.lower()].index
#     recommandations= similarities[movies_index][0]
#     movies_list = sorted(enumerate(recommandations), reverse=True, key=lambda x:x[1])[1:6]

#     recommand_movies = [movies.iloc[i[0]].title for i in movies_list]
#     # for i in movies_list:
#     #     print(movies.iloc[i[0]].title)
#     return recommand_movies

# movies=movies['title'].values
# name_movies = st.selectbox("Enter the Movie Name",movies)

# if st.button("Recommand Movies"):
#      r=recommand(name_movies)
#      st.write("Recommand Movies Ares")
#      for i in r:
#           st.write(i)
          
import streamlit as st
import pickle as p
import joblib as jl
import nltk
import pandas as pd

st.title("Movie Recommendation System")

# Load movie DataFrame
with open("movies.pickle", "rb") as movie_file:
    movies = p.load(movie_file)

# Load similarity matrix
similarities = jl.load("similarities.joblib")


def recommend(nameMovies):
    # Find index of selected movie
    movies_index = movies[movies["title"] == nameMovies].index[0]

    # Get similarity scores
    recommendations = similarities[movies_index]

    # Get top 5 similar movies
    movies_list = sorted(
        enumerate(recommendations),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]
 
    # Get movie titles
    recommended_movies = [
        movies.iloc[i[0]].title
        for i in movies_list
    ]

    return recommended_movies

# Keep DataFrame intact
movie_titles = movies["title"].values

nameMovies = st.selectbox(
    "Enter the Movie Name",
    movie_titles
)

if st.button("Recommend Movie"):
    recommended_movies = recommend(nameMovies)

    st.write("Recommended Movies Are:")
    for movie in recommended_movies:
        st.write(movie)