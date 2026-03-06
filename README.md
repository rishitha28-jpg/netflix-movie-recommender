# Netflix Movie Recommendation System

A Machine Learning based movie recommendation system that suggests similar movies based on **content similarity**.

The system uses **Content-Based Filtering with Cosine Similarity** to recommend movies based on movie metadata.

---

## Live Links

Backend API

https://netflix-movie-recommender-bxv3.onrender.com

API Documentation (Swagger)

https://netflix-movie-recommender-bxv3.onrender.com/docs

GitHub Repository

https://github.com/rishitha28-jpg/netflix-movie-recommender

---

## Project Overview

This project builds a **movie recommendation engine** similar to platforms like Netflix.

When a user selects a movie, the system finds other movies with similar characteristics using **machine learning similarity scores**.

The backend exposes REST APIs using **FastAPI**, which can be consumed by a frontend application.

---

## Features

- Recommend similar movies
- Search movies by name
- Trending movie suggestions
- REST API with FastAPI
- Deployed cloud backend using Render

---

## How the Recommendation System Works

The model follows a **Content-Based Recommendation approach**.

Steps:

1. Movie metadata (cast, crew, genres, keywords) are combined into a single feature called **tags**.
2. The text data is converted into numerical vectors using **CountVectorizer**.
3. Cosine Similarity is computed between movie vectors.
4. For a selected movie, the system returns the **Top N most similar movies**.

---

## Tech Stack

Backend  
FastAPI  
Python  

Machine Learning  
Pandas  
Scikit-Learn  

Deployment  
Render  

Frontend  
Streamlit  

---

## API Endpoints

### Home