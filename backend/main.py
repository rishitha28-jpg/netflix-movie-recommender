from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd
import os
import gdown

app = FastAPI()

# -------- BASE DIRECTORY --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------- MODELS DIRECTORY --------
models_dir = os.path.join(BASE_DIR, "models")
os.makedirs(models_dir, exist_ok=True)

movies_path = os.path.join(models_dir, "movies.pkl")
similarity_path = os.path.join(models_dir, "content_similarity.pkl")


# -------- DOWNLOAD MODELS --------
def download_models():

    if not os.path.exists(movies_path):
        print("Downloading movies.pkl")
        gdown.download(
            "https://drive.google.com/uc?id=19t9RKvI9D6fWek9_fdb43M62e4b9_h62",
            movies_path,
            quiet=False
        )

    if not os.path.exists(similarity_path):
        print("Downloading similarity model")
        gdown.download(
            "https://drive.google.com/uc?id=1vFvw7JG4oKX05a1deVNUO65mMYj8ndtt",
            similarity_path,
            quiet=False
        )


# -------- LOAD MODELS --------
movies = None
similarity = None


@app.on_event("startup")
def load_models():

    global movies, similarity

    download_models()

    movies = pickle.load(open(movies_path, "rb"))
    similarity = pickle.load(open(similarity_path, "rb"))

    movies = movies.reset_index(drop=True)
    movies["title"] = movies["title"].astype(str)

    print("Models loaded successfully")


# -------- HOME --------
@app.get("/")
def home():
    return {"message": "Netflix Movie Recommendation API running"}


# -------- RECOMMEND --------
@app.get("/recommend/{movie}")
def recommend(movie: str, n: int = 5):

    if movies is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    titles = movies["title"].str.lower()

    matches = movies[titles.str.contains(movie.lower(), na=False)]

    if matches.empty:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie_index = matches.index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:n+1]

    recommendations = []

    for i in movie_list:
        recommendations.append(movies.iloc[i[0]].title)

    return {
        "movie": movie,
        "recommendations": recommendations
    }


# -------- SEARCH --------
@app.get("/search/{query}")
def search(query: str):

    if movies is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    results = movies[
        movies["title"].str.contains(query, case=False, na=False)
    ]

    return {"results": results["title"].head(10).tolist()}


# -------- TRENDING --------
@app.get("/trending")
def trending():

    if movies is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    return {"movies": movies["title"].sample(10).tolist()}