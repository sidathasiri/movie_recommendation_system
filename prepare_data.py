def get_prepare_data():
    import pandas as pd

    movies = pd.read_csv("./movies.csv", encoding = "ISO-8859-1")
    movie_tags = pd.read_csv("./movie_tags.csv", encoding = "ISO-8859-1")
    movie_genre = pd.read_csv("./movie_genre.csv", encoding = "ISO-8859-1")

    processed_data = movies[["id", "title", "imdbID"]]
    processed_data = pd.merge(left=processed_data, right=movie_genre, left_on='id', right_on='movieID')
    del processed_data["movieID"]

    movie_genre_dict = {}
    for index, row in processed_data.iterrows():
        title = row['title']
        genre = row['genre']
        if(title not in movie_genre_dict):
            movie_genre_dict[title] = [genre]
        else:
    #         if(genre not in movie_genre_dict[title]):
            movie_genre_dict[title].append(genre)

    for key in movie_genre_dict.keys():
        movie_genre_dict[key] = " ".join(movie_genre_dict[key])

    movie_genre_processed = pd.DataFrame(list(movie_genre_dict.items()), columns = ["title", "genre"])

    imdb_list = []
    for index, row in movie_genre_processed.iterrows():
        title = row['title']
        imdb_list.append(movies.loc[movies['title'] == title].head(1).imdbID.values[0])

    movie_genre_processed['imdbID'] = imdb_list

    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer()
    X = cv.fit_transform(movie_genre_processed["genre"]).toarray()

    output = movie_genre_processed.loc[:,['title', "imdbID"]]
    output = output.join(pd.DataFrame(X))
    return [X, output]