from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]


def get_movies_by_search(query):
    # Searching for movies based on movieName
    return db.movies.find({
        "movieName": {"$regex": query, "$options": "i"}  # Case-insensitive search
    })
