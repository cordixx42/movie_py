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
netflixCol = mydb["netflix"]

#movieCol.delete_many({})
#netflixCol.delete_many({})


print(myclient.list_database_names())
print(mydb.list_collection_names())





# 1.1 - CLEANING MOVIELENS MOVIE DATA
movieData = pd.read_csv('movielens/movies.csv')
movieData['year'] = movieData['title'].str.extract(r'\((\d+)\)')
movieData = movieData.dropna()
movieData = movieData.drop(movieData[movieData['year'].str.len() < 4].index)

# remove year from title
movieData['title'] = movieData['title'].str.replace(r'\s\(\d+\)', '', regex=True)

# drop movies with no genre listed ?? rethink
# movieData = movieData.drop(movieData[movieData['genres'] == "(no genres listed)"].index)

# 1.2 - MERGE WITH NETFLIX
def normalize_v1(s):
    # Remove all non-alphanumeric characters (special characters)
    s = s.lower()
    return re.sub(r'[^a-zA-Z0-9]', '', s)

def normalize_v2(title):
    # Remove punctuation and spaces 
    title = title.lower()  
    title = re.sub(r'\s+', ' ', title)  
    title = re.sub(r'[^\w\s]', '', title) 
    return title.strip()  

netflixMovies = pd.read_json('whatsOnNetflix_2082025.json')
print(netflixMovies.head())
# NORMALIZATION MERGE using REGEX
netflixMoviesNorm = netflixMovies.copy()
movieDataNorm = movieData.copy()
netflixMoviesNorm['norm_title'] = netflixMoviesNorm['Title'].apply(normalize_v1)
movieDataNorm['norm_title'] = movieDataNorm['title'].apply(normalize_v1)

merged = pd.merge(netflixMoviesNorm, movieDataNorm, left_on=['norm_title', 'Release Year'], right_on=['norm_title','year'], how='inner')
netflixMovieIds = set(merged['movieId'])


# 1.3 - TAG PREPROCESSING
tagData = pd.read_csv('movielens/tags.csv')
#drop tags for movies not in our movie set
tagData = tagData.drop(tagData[~tagData['movieId'].isin(movieData['movieId'])].index)
#convert all tags to lower case 
tolower = lambda s: str(s).lower()
tagData['tag'] = tagData['tag'].apply(tolower)
#group by tag name 
tagData = tagData.groupby(['movieId', 'tag'])['userId'].nunique().reset_index(name='user_count')
tagData = tagData.sort_values(by='user_count', ascending=False)

# tags_for_movie = tagData.loc[tagData['movieId'] == 1, 'tag'].tolist()
# print(tags_for_movie)

# 1.4 - TMDB LINKS 
tmdbLinks = pd.read_csv('movielens/links.csv')


# insert into collection 
'''
all movielens movies 
{
movieId: int,
movieName: string,
releaseYear: string,
genres: [string],
tags: [string],
tmdbId: string/int
}
'''

'''
all netflix intersect movielens movies
{
movieId: int,
movieName: string,
releaseYear: string,
genres: [string],
tags: [string],
netflix: boolean,
language: [string],
tmdbId: string/int,
overview: string,
tagline: string,
tmdbRating: float,
posterLink: string, 
originalLanguage: string,
spokenLanguages: [string],
productionCompanies: [string],
overviewEmbedding: 
}
'''

""" i = 0 

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


    netflix = (movieId in netflixMovieIds)

    if netflix:
        print(tmdbId)
        print(i)
        i += 1

        #ADD API KEY 
        tmdb_api_key = ''
        tmdbData = TMDB_Metadata(tmdb_api_key, tmdbId)

        if 'Error' in tmdbData:
            continue

        embedding = model.encode(tmdbData['Overview'])

        myNetflixDict = {  "movieId": movieId, 
                            "movieName": movieName,
                            "releaseYear": releaseYear,
                            "genres": genres,
                            "tags": tags,
                            "tmdbId": tmdbId,
                            "overview": tmdbData['Overview'],
                            "tagline": tmdbData['Tagline'],
                            "tmdbRating": tmdbData['TMDB Rating'],
                            "posterLink": tmdbData['Poster'],
                            "originalLanguage": tmdbData['Origingal Language'],
                            "spokenLanguages": tmdbData['Spoken Languages'],
                            "productionCompanies": tmdbData['Production Companies'],
                            "overviewEmbedding": embedding.tolist()
                         }
        y = netflixCol.insert_one(myNetflixDict)
          """

# why 2324 instead of 2333
#print(mycol.count_documents({"netflix": True, "tags": []}))
print(netflixCol.count_documents({}))
print(netflixCol.count_documents({"tags": []}))
print(netflixCol.count_documents({"genres": []}))
print(netflixCol.count_documents({"tmdbId": None}))


# exporting all netflix data into json 
documents = netflixCol.find({},{"_id": 0, "movieId": 1, "movieName": 1, "releaseYear": 1, "genres": 1, "tags": 1, "originalLanguage": 1, "overview": 1, "overviewEmbedding": 1})
documentsList = list(documents)

with open('netflix_data_analysis.json', 'w') as file:
    json.dump(documentsList, file, indent=4)
 

# exporting all movielens data into json 
documents = movieCol.find({},{"_id": 0, "movieId": 1, "movieName": 1, "releaseYear": 1,  "genres": 1, "tags": 1,  "tmdbId": 1})
documentsList = list(documents)

with open('all_movie_data_analysis.json', 'w') as file:
    json.dump(documentsList, file, indent=4)


""" for x in mycol.find({"netflix": True},{ "_id": 0, "movieName": 1, "genres": 1, "tags": 1, "language": 1 }):
  print(x) """


