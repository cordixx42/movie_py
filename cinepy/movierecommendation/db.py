from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]


def get_movies_by_search(query):
    # Searching for movies based on movieName
    return db.movies.find({
        "movieName": {"$regex": query, "$options": "i"}  # Case-insensitive search
    })


def get_single_movie(movieId):
    return db.movies.find_one({
        "movieId": movieId
    })

def get_netflix_movies(tmdbIdList):
    cursor = db.netflixTmdb.find({
        'tmdbId': {'$in': tmdbIdList}
    })
    movies_sorted = sorted(cursor, key=lambda movie: tmdbIdList.index(movie['tmdbId']))
    return movies_sorted
