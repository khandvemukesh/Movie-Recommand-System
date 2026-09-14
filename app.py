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

#-----------------------------------------Steamlit Code---------------------------------------------    
# import streamlit as st
# import pickle as p
# import joblib as jl
# import nltk
# import pandas as pd
# import numpy as np


# st.title("Movie Recommendation System")

# # Load movie DataFrame
# with open("movies.pickle", "rb") as movie_file:
#     movies = p.load(movie_file)

# # Load similarity matrix
# similarities = jl.load("similarities.joblib")


# def recommend(nameMovies):
#     # Find index of selected movie
#     movies_index = movies[movies["title"] == nameMovies].index[0]

#     # Get similarity scores
#     recommendations = similarities[movies_index]

#     # Get top 5 similar movies
#     movies_list = sorted(
#         enumerate(recommendations),
#         reverse=True,
#         key=lambda x: x[1]
#     )[1:6]
 
#     # Get movie titles
#     recommended_movies = [
#         movies.iloc[i[0]].title
#         for i in movies_list
#     ]

#     return recommended_movies

# # Keep DataFrame intact
# movie_titles = movies["title"].values

# nameMovies = st.selectbox(
#     "Enter the Movie Name",
#     movie_titles
# )

# if st.button("Recommend Movie"):
#     recommended_movies = recommend(nameMovies)

#     st.write("Recommended Movies Are:")
#     for movie in recommended_movies:
#         st.write(movie)

#-----------------------------------------Steamlit Code---------------------------------------------

#----------------------------------------- Flask Code---------------------------------------------
from flask import Flask, request, jsonify
import pickle as p 
import joblib as jl 
from flask_cors import CORS

app = Flask(__name__) 
CORS(app)
# ----------------------------- # Load movie DataFrame # ----------------------------- 

with open("movies.pickle", "rb") as movie_file: movies = p.load(movie_file)

# ----------------------------- # Load similarity matrix # ----------------------------- 

similarities = jl.load("similarities.joblib")

# ----------------------------- # Recommendation function # ----------------------------- 

def recommend(nameMovies): # Find index of selected movie 
    movie_matches = movies[movies["title"] == nameMovies] # Movie not found 
    if movie_matches.empty: return [] 
    movies_index = movie_matches.index[0] # Get similarity scores 
    recommendations = similarities[movies_index] # Get top 5 similar movies 
    movies_list = sorted( enumerate(recommendations), reverse=True, key=lambda x: x[1] )[1:6] # Get movie titles 
    recommended_movies = [ movies.iloc[i[0]]["title"] for i in movies_list ] 
    return recommended_movies

# Home route
@app.route("/", methods=["GET"]) 
def home(): 
    return jsonify({ "message": "Movie Recommendation API is running" })

# Get all Movies Titles
@app.route("/movies", methods=["GET"]) 
def get_movies(): 
    movie_titles = movies["title"].dropna().tolist() 
    return jsonify({ "movies": movie_titles })

# Get Recommended movies
@app.route("/recommend", methods=["POST"]) 
def recommend_movies(): 
    data = request.get_json() 
    if not data or "movie" not in data: 
        return jsonify({ "error": "Please provide a movie name" }), 400 
    movie_name = data["movie"] 
    recommended_movies = recommend(movie_name) 
    if not recommended_movies: 
        return jsonify({ "error": "Movie not found" }), 404 
    return jsonify({ "movie": movie_name, "recommendations": recommended_movies })

if __name__ == "__main__":
    app.run(host="https://movie-recommand-system.vercel.app", debug=True)