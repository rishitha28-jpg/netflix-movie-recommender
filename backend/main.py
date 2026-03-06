# from fastapi import FastAPI
# from src.recommender import content_recommend


# app = FastAPI()


# @app.get("/")
# def home():

#     return {"message": "Movie Recommendation API Running"}


# @app.get("/recommend/{movie}")
# def recommend(movie: str):

#     recommendations = content_recommend(movie)

#     return {"recommendations": recommendations}
from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd

app = FastAPI(
    title="Netflix Movie Recommendation API",
    description="Movie recommendation API using content-based filtering",
    version="1.0.0"
)

similarity = None
movies = None


# ---------- LOAD MODELS ----------
@app.on_event("startup")
def load_models():
    global similarity, movies

    similarity = pickle.load(open("models/content_similarity.pkl", "rb"))
    movies = pickle.load(open("models/movies.pkl", "rb"))


# ---------- HOME ----------
@app.get("/")
def home():
    return {"message": "Netflix Movie Recommendation API Running"}


# ---------- HEALTH CHECK ----------
@app.get("/health")
def health():
    return {"status": "API running"}


# ---------- RECOMMEND ----------
@app.get("/recommend/{movie}")
def recommend(movie: str, n: int = 5):

    movie_lower = movie.lower()

    titles = movies["title"].str.lower()

    if movie_lower not in titles.values:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie_index = movies[titles == movie_lower].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:n+1]

    recommendations = [
        movies.iloc[i[0]].title for i in movie_list
    ]

    return {"movie": movie, "recommendations": recommendations}


# ---------- TRENDING ----------
@app.get("/trending")
def trending(n: int = 10):

    trending_movies = movies["title"].sample(n).tolist()

    return {"movies": trending_movies}


# ---------- SEARCH ----------
@app.get("/search/{query}")
def search(query: str, n: int = 10):

    results = movies[
        movies["title"].str.contains(query, case=False)
    ]

    return {"results": results["title"].head(n).tolist()}