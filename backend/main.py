# from fastapi import FastAPI, HTTPException
# import pickle
# import pandas as pd
# import os

# app = FastAPI(
#     title="Netflix Movie Recommendation API",
#     description="Movie recommendation API using content-based filtering",
#     version="1.0.0"
# )

# similarity = None
# movies = None


# # ---------- GET BASE DIRECTORY ----------
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# # ---------- LOAD MODELS ----------
# @app.on_event("startup")
# def load_models():
#     global similarity, movies

#     similarity_path = os.path.join(BASE_DIR, "models", "content_similarity.pkl")
#     movies_path = os.path.join(BASE_DIR, "models", "movies.pkl")

#     similarity = pickle.load(open(similarity_path, "rb"))
#     movies = pickle.load(open(movies_path, "rb"))


# # ---------- HOME ----------
# @app.get("/")
# def home():
#     return {"message": "Netflix Movie Recommendation API Running"}


# # ---------- HEALTH CHECK ----------
# @app.get("/health")
# def health():
#     return {"status": "API running"}


# # ---------- RECOMMEND ----------
# @app.get("/recommend/{movie}")
# def recommend(movie: str, n: int = 5):

#     movie_lower = movie.lower()

#     titles = movies["title"].str.lower()

#     if movie_lower not in titles.values:
#         raise HTTPException(status_code=404, detail="Movie not found")

#     movie_index = movies[titles == movie_lower].index[0]

#     distances = similarity[movie_index]

#     movie_list = sorted(
#         list(enumerate(distances)),
#         key=lambda x: x[1],
#         reverse=True
#     )[1:n+1]

#     recommendations = [
#         movies.iloc[i[0]].title for i in movie_list
#     ]

#     return {
#         "movie": movie,
#         "recommendations": recommendations
#     }


# # ---------- TRENDING ----------
# @app.get("/trending")
# def trending(n: int = 10):

#     trending_movies = movies["title"].sample(n).tolist()

#     return {"movies": trending_movies}


# # ---------- SEARCH ----------
# @app.get("/search/{query}")
# def search(query: str, n: int = 10):

#     results = movies[
#         movies["title"].str.contains(query, case=False)
#     ]

#     return {"results": results["title"].head(n).tolist()}
from fastapi import FastAPI, HTTPException
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

app = FastAPI(
    title="Netflix Movie Recommendation API",
    description="Movie recommendation API using content-based filtering",
    version="1.0.0"
)

movies = None
similarity = None


# ---------- BASE DIRECTORY ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------- LOAD DATA ----------
@app.on_event("startup")
def load_models():
    global movies, similarity

    movies_path = os.path.join(BASE_DIR, "data", "movies.csv")

    movies = pd.read_csv(movies_path)

    # create tags column from available text columns
    movies["tags"] = (
        movies["overview"].fillna("").astype(str) + " " +
        movies["genres"].fillna("").astype(str)
    )

    cv = CountVectorizer(max_features=5000, stop_words="english")

    vectors = cv.fit_transform(movies["tags"]).toarray()

    similarity = cosine_similarity(vectors)


# ---------- HOME ----------
@app.get("/")
def home():
    return {"message": "Netflix Movie Recommendation API Running"}


# ---------- HEALTH ----------
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

    return {
        "movie": movie,
        "recommendations": recommendations
    }


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