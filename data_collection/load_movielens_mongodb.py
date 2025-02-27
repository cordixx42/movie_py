import pymongo
import pandas as pd 
import re
from tmdb_search import *
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import bson
import json

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Lightweight and fast model

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["moviepy"]
movieCol = mydb["movies"]

#movieCol.delete_many({})
#netflixCol.delete_many({})

# 1.1 - CLEANING MOVIELENS MOVIE DATA
movieData = pd.read_csv('movielens/movies.csv')
movieData['year'] = movieData['title'].str.extract(r'\((\d+)\)')
movieData = movieData.dropna()
movieData = movieData.drop(movieData[movieData['year'].str.len() < 4].index)

# remove year from title
movieData['title'] = movieData['title'].str.replace(r'\s\(\d+\)', '', regex=True)


# 1.2 - TAG PREPROCESSING
tagData = pd.read_csv('movielens/tags.csv')
#drop tags for movies not in our movie set
tagData = tagData.drop(tagData[~tagData['movieId'].isin(movieData['movieId'])].index)
#convert all tags to lower case 
tolower = lambda s: str(s).lower()
tagData['tag'] = tagData['tag'].apply(tolower)
#group by tag name 
tagData = tagData.groupby(['movieId', 'tag'])['userId'].nunique().reset_index(name='user_count')
tagData = tagData.sort_values(by='user_count', ascending=False)


# 1.3 - TMDB LINKS 
tmdbLinks = pd.read_csv('movielens/links.csv')


# 1.4 - INSERTING MOVIELENS MOVIES INTO THE COLLECTION MOVIES IN MONGODB DATABASE (more than 80000 movies)

'''
data model
{
movieId: int,
movieName: string,
releaseYear: string,
genres: [string],
tags: [string],
tmdbId: float
}
'''

i = 0 
for index, row in movieData.iterrows():
    movieId = row['movieId']
    movieName = row['title']
    releaseYear = row['year']
    genres = list()
    sepGenreList = movieData.loc[index]['genres'].split(sep='|')
    for g in sepGenreList:
        if g != '(no genres listed)':
            genres.append(g)

    tags = tagData.loc[tagData['movieId'] == movieId, 'tag'].tolist()
    
    tmdbLink = tmdbLinks.loc[tmdbLinks['movieId'] == movieId, 'tmdbId']

    tmdbId = None
    if not pd.isna(tmdbLink).any():
        tmdbId = tmdbLink.iloc[0] 
    
    
    mydict = { "movieId": movieId, 
               "movieName": movieName,
               "releaseYear": releaseYear,
               "genres": genres,
               "tags": tags,
               "tmdbId": tmdbId
                }
    

    x = movieCol.insert_one(mydict)


# 1.5 - EXPORTING DATA INTO JSON 

"""
# exporting all movielens data into json 
documents = movieCol.find({},{"_id": 0, "movieId": 1, "movieName": 1, "releaseYear": 1,  "genres": 1, "tags": 1,  "tmdbId": 1})
documentsList = list(documents)

with open('all_movie_data_analysis.json', 'w') as file:
    json.dump(documentsList, file, indent=4) """





