import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
TMDB_KEY = "2acecd8f5497e05fb04b7744f230aba2"

st.set_page_config(page_title="Netflix Recommender", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>

.stApp{
background-color:#0e1117;
}

/* NETFLIX TITLE */
.title{
text-align:center;
font-size:70px;
color:#E50914;
font-weight:900;
margin-top:20px;
margin-bottom:10px;
letter-spacing:2px;
}

/* SUBTITLE */
.subtitle{
text-align:center;
color:white;
font-size:20px;
margin-bottom:40px;
}

/* SECTION HEADINGS */
.section{
font-size:30px;
color:white;
margin-top:40px;
margin-bottom:20px;
font-weight:bold;
}

/* MOVIE TITLE */
.movie-title{
color:white;
font-weight:bold;
text-align:center;
margin-top:8px;
font-size:16px;
}

/* SEARCH LABEL */
label{
color:white !important;
}

/* SEARCH BOX */
input{
background-color:#1f1f1f !important;
color:white !important;
border-radius:8px !important;
padding:10px !important;
border:1px solid #444 !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<p class="title">🎬 Netflix Movie Recommender</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover movies similar to your favorites</p>', unsafe_allow_html=True)


# ---------- FETCH POSTER ----------
def fetch_poster(movie_name):

    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&query={movie_name}"

    try:
        data = requests.get(url).json()

        if len(data["results"]) == 0:
            return None, None, None

        movie = data["results"][0]

        poster = movie.get("poster_path")
        rating = movie.get("vote_average")
        release = movie.get("release_date")

        poster_url = None
        if poster:
            poster_url = "https://image.tmdb.org/t/p/w500/" + poster

        year = release[:4] if release else "N/A"

        return poster_url, rating, year

    except:
        return None, None, None


# ---------- SEARCH ----------
movie = st.text_input(
    "🔍 Search for a movie",
    placeholder="Example: Avatar, Titanic, Iron Man"
)

# ---------- AUTOCOMPLETE ----------
if movie:

    try:
        suggestions = requests.get(f"{API_URL}/search/{movie}").json()["results"]

        if suggestions:
            st.markdown(
                f"<p style='color:white'>Suggestions: {', '.join(suggestions[:5])}</p>",
                unsafe_allow_html=True
            )

    except:
        pass


# ---------- RECOMMEND ----------
if st.button("Recommend"):

    with st.spinner("Finding similar movies... 🎬"):

        try:

            res = requests.get(f"{API_URL}/recommend/{movie}")
            movies = res.json()["recommendations"]

            st.markdown('<p class="section">Recommended For You</p>', unsafe_allow_html=True)

            cols = st.columns(5)

            for col, m in zip(cols, movies):

                with col:

                    poster, rating, year = fetch_poster(m)

                    if poster:
                        st.image(poster, use_container_width=True)

                    st.markdown(f'<p class="movie-title">{m}</p>', unsafe_allow_html=True)

                    if rating:
                        st.markdown(
                            f"<p style='text-align:center;color:white'>⭐ {rating}</p>",
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        f"<p style='text-align:center;color:white'>📅 {year}</p>",
                        unsafe_allow_html=True
                    )

        except:
            st.error("Recommendation API error")


# ---------- TRENDING ----------
st.markdown('<p class="section">Trending Movies</p>', unsafe_allow_html=True)

try:
    trend = requests.get(f"{API_URL}/trending").json()["movies"]
except:
    trend = []

cols = st.columns(5)

for col, m in zip(cols, trend[:5]):

    with col:

        poster, rating, year = fetch_poster(m)

        if poster:
            st.image(poster, use_container_width=True)

        st.markdown(f'<p class="movie-title">{m}</p>', unsafe_allow_html=True)


# ---------- POPULAR ----------
st.markdown('<p class="section">Popular Movies</p>', unsafe_allow_html=True)

cols = st.columns(5)

for col, m in zip(cols, trend[5:10]):

    with col:

        poster, rating, year = fetch_poster(m)

        if poster:
            st.image(poster, use_container_width=True)

        st.markdown(f'<p class="movie-title">{m}</p>', unsafe_allow_html=True)


# ---------- FOOTER ----------
st.markdown("""
<hr style="border:1px solid #333; margin-top:50px">

<div style="text-align:center;color:#aaaaaa;font-size:14px">

🎬 <b>Netflix Movie Recommendation System</b><br><br>

Built with <b>FastAPI</b> • <b>Streamlit</b> • <b>TMDB API</b><br>

Machine Learning: <b>Content-Based Recommendation System</b>

</div>
""", unsafe_allow_html=True)