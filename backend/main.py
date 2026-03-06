from fastapi import FastAPI, HTTPException
import pickle
import os
import gdown
import random

app = FastAPI()

# -------- PATHS --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
models_dir = os.path.join(BASE_DIR, "models")
os.makedirs(models_dir, exist_ok=True)

similarity_path = os.path.join(models_dir, "content_similarity.pkl")


# -------- DOWNLOAD MODEL --------
def download_model():
    if not os.path.exists(similarity_path):
        print("Downloading similarity model...")
        gdown.download(
            "https://drive.google.com/uc?id=1vFvw7JG4oKX05a1deVNUO65mMYj8ndtt",
            similarity_path,
            quiet=False
        )


# -------- GLOBAL VARIABLE --------
similarity = None


# -------- LOAD MODEL --------
@app.on_event("startup")
def load_model():
    global similarity

    download_model()
    similarity = pickle.load(open(similarity_path, "rb"))

    print("Similarity model loaded successfully")


# -------- HOME --------
@app.get("/")
def home():
    return {"message": "Netflix Movie Recommendation API running"}


# -------- RECOMMEND --------
@app.get("/recommend/{movie}")
def recommend(movie: str, n: int = 5):

    if similarity is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    movie_index = random.randint(0, len(similarity) - 1)

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:n+1]

    recommendations = [str(i[0]) for i in movie_list]

    return {
        "movie": movie,
        "recommendations": recommendations
    }


# -------- TRENDING --------
@app.get("/trending")
def trending():

    if similarity is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    movies = random.sample(range(len(similarity)), 10)

    return {"movies": [str(i) for i in movies]}


# -------- SEARCH --------
@app.get("/search/{query}")
def search(query: str):
    return {"results": ["Movie1", "Movie2", "Movie3"]}