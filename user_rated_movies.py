import pandas as pd

ratings = pd.read_csv("./user_rated_movies.csv", encoding = "ISO-8859-1")
movies = pd.read_csv("./movies.csv", encoding = "ISO-8859-1")

def get_latest_rated_movie(uid):
    time = ratings.loc[ratings["ï»¿userID"]==uid,["movieID","timestamp"]]
    latest_movieIds_watched_by_user = time.sort_values(by="timestamp",ascending=False)["movieID"].values[:5]
    print("latest movie ids:", latest_movieIds_watched_by_user)
    imdb_movie_ids = []
    for id in latest_movieIds_watched_by_user:
        imdb_movie_ids.append(movies.loc[movies['id'] == id].head(1).imdbID.values[0])
    return imdb_movie_ids

def get_latest_rated_movie_ids(uid):
    time = ratings.loc[ratings["ï»¿userID"]==uid,["movieID","timestamp"]]
    latest_movieIds_watched_by_user = time.sort_values(by="timestamp",ascending=False)["movieID"].values[:5]
    # print("latest movie ids:", latest_movieIds_watched_by_user)
    return latest_movieIds_watched_by_user

def get_genre_by_imdb_id(id):
    movies.loc[movies['imdbID'] == id].head(1).id.values[0]

def get_users():
    return list(set(ratings["ï»¿userID"].values))

