# import get_prepare_data from './prepare_data'

from prepare_data import get_prepare_data
from user_rated_movies import get_latest_rated_movie
import pandas as pd

[X, output] = get_prepare_data()

from sklearn.metrics.pairwise import cosine_similarity
similarities = cosine_similarity(X) 

def get_movie_by_index(idx):
    return output.iloc[idx].title
def get_movie_by_imdb_id(mv_id):
    return output.loc[output['imdbID']==mv_id,['title']].values[0][0]

def find_similar_movies_indexes(imdb_id):
    record_id = output.loc[output['imdbID']==imdb_id,["title"]].index[0]
    similarity_values = pd.Series(similarities[record_id])
#     print(similarity_values)
    similarity_values = similarity_values.sort_values(ascending=False)
    # print(similarity_values)
    similarity_movie_indexes = list(similarity_values.index) 
    similarity_movie_indexes.remove(record_id)
    return similarity_movie_indexes[:5]

import flask
from flask import jsonify
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    uid = int(request.args.get('uid'))
    imdb_ids = get_latest_rated_movie(int(uid))
    print('Finding recommendations for ', imdb_ids)
    similar_movies = []
    for im_id in imdb_ids:
        similar_movie_idxes = find_similar_movies_indexes(im_id)
        for id in similar_movie_idxes:
            similar_movies.append(get_movie_by_index(id))
    return jsonify({
        "recommended_movies": similar_movies
    })

app.run()
