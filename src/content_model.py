import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import load_data


df = load_data()

# convert text to vectors
tfidf = TfidfVectorizer(stop_words="english")

vectors = tfidf.fit_transform(df["tags"])

# compute similarity matrix
similarity = cosine_similarity(vectors)

# save models
pickle.dump(similarity, open("models/content_similarity.pkl", "wb"))
pickle.dump(df, open("models/movies.pkl", "wb"))

print("Content-based model trained successfully")