import pandas as pd 
import pymongo
import re
from tmdb_search import *
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import matplotlib.pyplot as plt


model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Lightweight and fast model

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["moviepy"]
netflixTmdbCol = mydb["netflixTmdb"]

netflixMovies = pd.read_json('whatsOnNetflix_2082025.json')
print(netflixMovies.head())

# 1.1 - TAG PREPROCESSING
tagData = pd.read_csv('movielens/tags.csv')
#convert all tags to lower case 
tolower = lambda s: str(s).lower()
tagData['tag'] = tagData['tag'].apply(tolower)
#group by tag name 
tagData = tagData.groupby(['movieId', 'tag'])['userId'].nunique().reset_index(name='user_count')
tagData = tagData.sort_values(by='user_count', ascending=False)

# 1.2 - TMDB LINKS 
tmdbLinks = pd.read_csv('movielens/links.csv')


# 1.3 - INSERTING NETFLIX MOVIES MERGED WITH TMDB DATA INTO NETFLIXTMDB COLLECTION IN MONGODB DATABASE (more than 4000 movies)

'''
data model
{
tmdbId: string/int,
movieName: string,
releaseYear: string,
genres: [string],
tags: [string],
overview: string,
tagline: string,
tmdbRating: float,
posterLink: string, 
originalLanguage: string,
spokenLanguages: [string],
productionCompanies: [string],
overviewEmbedding: [byte]
}
'''

errcount = 0 
errcount2 = 0

for index, row in netflixMovies.iterrows():
    print(index)
    tmdb_api_key = ''
    tmdbData = TMDB_Metadata(tmdb_api_key, row['Title'], 0)

    if 'Error' in tmdbData:
        errcount += 1
        continue
    else:
    
        movielens = tmdbLinks.loc[tmdbLinks['tmdbId'] == tmdbData['ID'], 'movieId']

        movielensId = None
        tags = []
        if not (pd.isna(movielens).any() or movielens.empty):
            movielensId = movielens.iloc[0] 
            tags = tagData.loc[tagData['movieId'] == movielensId, 'tag'].tolist()
        else:
            errcount2 += 1

        embedding = model.encode(tmdbData['Overview'])

        myNetflixTmdbDict = {   "tmdbId": tmdbData['ID'], 
                                "movieName": tmdbData['Title'],
                                "releaseYear": tmdbData['Release'],
                                "genres":  tmdbData['Genres'],
                                "tags": tags,
                                "overview": tmdbData['Overview'],
                                "tagline": tmdbData['Tagline'],
                                "tmdbRating": tmdbData['TMDB Rating'],
                                "posterLink": tmdbData['Poster'],
                                "originalLanguage": tmdbData['Origingal Language'],
                                "spokenLanguages": tmdbData['Spoken Languages'],
                                "productionCompanies": tmdbData['Production Companies'],
                                "overviewEmbedding": embedding.tolist()
                         }
        y = netflixTmdbCol.insert_one(myNetflixTmdbDict)

print(f'movies not matched in tmdb {errcount}')
print(f'movies not matched in movielens {errcount2}')

# 1.4 - EXPORT DATA INTO JSON 

""" documents = netflixTmdbCol.find({},{"_id": 0, "tmdbId": 1, "movieName": 1, "releaseYear": 1, "genres": 1, "tags": 1, "originalLanguage": 1, "overview": 1, "overviewEmbedding": 1})
documentsList = list(documents)

with open('netflix_tmdb_match.json', 'w') as file:
    json.dump(documentsList, file, indent=4) """