import pandas as pd
import pickle
from surprise import Dataset, Reader, SVD


df = pd.read_csv("data/movies.csv")

reader = Reader(rating_scale=(1, 5))

data = Dataset.load_from_df(
    df[['userId', 'movieId', 'rating']],
    reader
)

trainset = data.build_full_trainset()

model = SVD()

model.fit(trainset)

pickle.dump(model, open("models/collaborative_model.pkl", "wb"))

print("Collaborative filtering model trained successfully")