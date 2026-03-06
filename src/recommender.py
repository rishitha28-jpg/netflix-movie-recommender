# import pickle


# # load models
# similarity = pickle.load(open("models/content_similarity.pkl", "rb"))
# movies = pickle.load(open("models/movies.pkl", "rb"))


# def content_recommend(movie):

#     movie_index = movies[movies['title'] == movie].index[0]

#     distances = similarity[movie_index]

#     movie_list = sorted(
#         list(enumerate(distances)),
#         reverse=True,
#         key=lambda x: x[1]
#     )[1:6]

#     recommendations = []

#     for i in movie_list:
#         recommendations.append(movies.iloc[i[0]].title)

#     return recommendations
import pickle
import pandas as pd


# ---------- LOAD MODELS ----------
similarity = pickle.load(open("models/content_similarity.pkl", "rb"))
movies = pickle.load(open("models/movies.pkl", "rb"))


# ---------- CONTENT RECOMMENDATION ----------
def content_recommend(movie: str, n: int = 5):
    """
    Return top N recommended movies based on cosine similarity.
    """

    movie = movie.lower()

    titles = movies["title"].str.lower()

    # movie not found
    if movie not in titles.values:
        return fallback_movies(n)

    movie_index = movies[titles == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:n+1]

    recommendations = [
        movies.iloc[i[0]].title for i in movie_list
    ]

    return recommendations


# ---------- FALLBACK POPULAR MOVIES ----------
def fallback_movies(n: int = 5):
    """
    Return random movies if input movie is not found.
    """

    return movies["title"].sample(n).tolist()


# ---------- SEARCH MOVIES ----------
def search_movies(query: str, n: int = 10):
    """
    Search movies using partial match.
    Used for autocomplete.
    """

    results = movies[
        movies["title"].str.contains(query, case=False, na=False)
    ]

    return results["title"].head(n).tolist()


# ---------- TRENDING MOVIES ----------
def trending_movies(n: int = 10):
    """
    Return random trending movies.
    """

    return movies["title"].sample(n).tolist()