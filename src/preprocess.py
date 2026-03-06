import pandas as pd

def load_data():

    df = pd.read_csv("data/movies.csv")

    # keep required columns
    df = df[['movie_id', 'title', 'cast', 'crew']]

    # remove missing values
    df = df.dropna()

    # feature engineering
    df["tags"] = df["cast"] + " " + df["crew"]

    return df