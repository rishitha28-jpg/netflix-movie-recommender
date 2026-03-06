from fastapi import FastAPI, HTTPException
import pickle
import os
import gdown
import pandas as pd

app = FastAPI()

# -------- PATHS --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
models_dir = os.path.join(BASE_DIR, "models")
os.makedirs(models_dir, exist_ok=True)

movies_path = os.path.join(models_dir, "movies.pkl")
similarity_path = os.path.join(models_dir, "content_similarity.pkl")


# -------- DOWNLOAD MODELS --------
def download_models():

    # correct movies.pkl
    if not os.path.exists(movies_path):
        print("Downloading movies.pkl")
        gdown.download(
            "https://drive.google.com/uc?id=1vFvw7JG4oKX05a1deVNUO65mMYj8ndtt",
            movies_path,
            quiet=False
        )

    # correct similarity.pkl
    if not os.path.exists(similarity_path):
        print("Downloading content_similarity.pkl")
        gdown.download(
            "https://drive.google.com/uc?id=19t9RKvI9D6fWek9_fdb43M62e4b9_h62",
            similarity_path,
            quiet=False
        )


movies = None
similarity = None


# -------- LOAD MODELS --------
@app.on_event("startup")
def load_models():

    global movies, similarity

    download_models()

    movies = pickle.load(open(movies_path, "rb"))
    similarity = pickle.load(open(similarity_path, "rb"))

    # ensure dataframe
    if not isinstance(movies, pd.DataFrame):
        movies = pd.DataFrame(movies)

    # ensure title column
    if "title" not in movies.columns:
        movies["title"] = movies.iloc[:, 0]

    movies["title"] = movies["title"].astype(str)

    # ensure numpy array
    if isinstance(similarity, pd.DataFrame):
        similarity = similarity.values

    print("Models loaded successfully")


# -------- HOME --------
@app.get("/")
def home():
    return {"message": "Netflix Movie Recommendation API running"}


# -------- RECOMMEND --------
@app.get("/recommend/{movie}")
def recommend(movie: str, n: int = 5):

    movie = movie.lower()

    matched_movies = movies[
        movies["title"].str.lower().str.contains(movie)
    ]

    if matched_movies.empty:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie_index = matched_movies.index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:n+1]

    recommendations = [
        movies.iloc[i[0]].title for i in movie_list
    ]

    return {
        "movie_found": movies.iloc[movie_index].title,
        "recommendations": recommendations
    }


# -------- SEARCH --------
@app.get("/search/{query}")
def search(query: str):

    results = movies[
        movies["title"].str.contains(query, case=False, na=False)
    ]

    return {
        "results": results["title"].head(10).tolist()
    }


# -------- TRENDING --------
@app.get("/trending")
def trending():

    return {
        "movies": movies["title"].sample(10).tolist()
    }


# -------- MOVIES LIST --------
@app.get("/movies")
def get_movies():

    return {
        "movies": movies["title"].head(100).tolist()
    }