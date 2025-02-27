from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

# Searching for movies based on movieName
def get_movies_by_search(query):
    return db.movies.find({
        "movieName": {"$regex": query, "$options": "i"}  # Case-insensitive search
    })

# Searching for movie based on movieId
def get_single_movie(movieId):
    return db.movies.find_one({
        "movieId": movieId
    })

# Searching for movies based on movieId list
def get_netflix_movies(tmdbIdList):
    cursor = db.netflixTmdb.find({
        'tmdbId': {'$in': tmdbIdList}
    })
    movies_sorted = sorted(cursor, key=lambda movie: tmdbIdList.index(movie['tmdbId']))
    return movies_sorted
