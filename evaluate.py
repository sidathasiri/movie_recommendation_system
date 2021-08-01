from user_rated_movies import get_latest_rated_movie_ids
from prepare_data import get_prepare_data
from user_rated_movies import get_users
import requests
import pandas as pd
from collections import Counter

movie_genre = pd.read_csv("./movie_genre.csv", encoding = "ISO-8859-1")
[X, output, movie_genre_processed] = get_prepare_data()

def get_genre_by_movie_id(id):
    movie_genres = movie_genre.loc[movie_genre['movieID'] == id]
    # print('genre for id:', id)
    # print('genres:', movie_genres.genre.values)
    return movie_genres.genre.values

def get_most_watched_genres(genres):
    freq = dict(Counter(genres)) 
    sorted_freq = {k: v for k, v in sorted(freq.items(), key=lambda item: item[1])}
    # print(sorted_freq)
    keys = list(sorted_freq.keys())
    # print(keys)
    if(len(keys)>3):
        return keys[-3:]
    return keys

total_score = 0
user_count = 50
users = get_users()[:user_count]

for uid in users:
    user_fav_movies = get_latest_rated_movie_ids(uid)
    # print(user_fav_movies)
    fav_movie_genres = []
    for mov in user_fav_movies:
        fav_movie_genres.extend(get_genre_by_movie_id(mov))
    most_fav_genres = get_most_watched_genres(fav_movie_genres) 
    # print(most_fav_genres)
    # print('fav movie genres:', most_fav_genres)
    req = requests.get("http://127.0.0.1:5000/?uid="+str(uid))
    recommended_movies = dict(req.json())['recommended_movies']
    # print(recommended_movies)
    incorrect_reccomendations = 0 
    for movie in recommended_movies:
        recommended_movie_genres = list(set(movie_genre_processed.loc[movie_genre_processed['title'] == movie]["genre"].values[0].split(" ")))
        # print(movie, recommended_movie_genres)
        matching_genre = False
        for genre in recommended_movie_genres:
            if (genre in most_fav_genres):
                matching_genre = True
                break
        if(matching_genre == False):
            # print('incorrect recommendation:', movie)
            incorrect_reccomendations = incorrect_reccomendations + 1
    user_score = 1-(incorrect_reccomendations/len(recommended_movies))
    print("User_id:", uid, "User_score:", user_score)
    total_score = total_score + user_score

print('total_score', total_score/user_count)

