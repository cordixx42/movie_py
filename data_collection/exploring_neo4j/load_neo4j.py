import pandas as pd 
from data_collection.exploring_neo4j.neo4j_init import *
from itertools import pairwise
import numpy as np 
import re

pd.set_option('display.max_columns', None)

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "12345678")

# 1 - LOADING ALL MOVIE LENS DATA INTO NEO4J 


# 1.1 - CLEANING MOVIELENS MOVIE DATA
movieData = pd.read_csv('movielens/movies.csv')
movieData['year'] = movieData['title'].str.extract(r'\((\d+)\)')
movieData = movieData.dropna()
movieData = movieData.drop(movieData[movieData['year'].str.len() < 4].index)

# remove year from title
movieData['title'] = movieData['title'].str.replace(r'\s\(\d+\)', '', regex=True)

# drop movies with no genre listed ?? rethink
# movieData = movieData.drop(movieData[movieData['genres'] == "(no genres listed)"].index)


driver = getDriver()

""" # 1.2 - CREATING YEAR NODES
allYears = set(movieData['year'].drop_duplicates())
for y in allYears:
    addYear(driver,y)

print('done creating years')


# 1.2 - CREATING GENRE NODES
genreSet = {'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 
            'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
            'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'}

for g in genreSet:
    addGenre(driver,g)

print('done creating genres')

# 1.3 - CREATE MOVIES AND ADD MOVIE TO YEAR AND GENRE RELATION 
for index, row in movieData.iterrows():
    addMovie(driver, row['title'], row['movieId'])
    addMovieYearRelation(driver, row['movieId'], row['year'])
    sepGenreList = movieData.loc[index]['genres'].split(sep='|')
    for g in sepGenreList:
        addMovieGenreRelation(driver, row['movieId'], g)

print('done creating movies and movie genre year relation')

# 1.4 - TAG PREPROCESSING 
tagData = pd.read_csv('movielens/tags.csv')
#drop tags for movies not in our movie set
tagData = tagData.drop(tagData[~tagData['movieId'].isin(movieData['movieId'])].index)
#convert all tags to lower case 
tolower = lambda s: str(s).lower()
tagData['tag'] = tagData['tag'].apply(tolower)
#group by tag name 
tagData = tagData.groupby(['movieId', 'tag'])['userId'].nunique().reset_index(name='user_count')
tagData = tagData.sort_values(by='user_count', ascending=False)

print(tagData.describe())
tagData = tagData.head(50000)

tags = tagData['tag'].drop_duplicates()
movies = tagData['movieId'].drop_duplicates()

# print(len(tags)) # 9002
# print(len(movies)) # 5883

# 1.5 - CREATING TAG NODES
for t in tags:
    addTag(driver, t)

print('done creating tags')

# 1.5 - CREATING MOVIE TAG RELATIONS
for index, row in tagData.iterrows():
    addMovieTagRelation(driver, row['movieId'], row['tag'])

print('done done')

 """

# 1.6 - CREATING A NETFLIX NODE WHICH ALL MOVIES IN NETFLIX ARE CONNECTED TO
addNetflixNode(driver)



# 1.7 - getting intersection of movielens and netflix movies 

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


# 1.8 - add languages 
for l in merged['Language'].drop_duplicates():
    addLanguageNode(driver, l)

# 1.9 - add movie language and movie netflix relation
for index, row in merged.iterrows():
    addMovieLanguageRelation(driver, row['movieId'], row['Language'])
    addMovieNetflixRelation(driver, row['movieId'])
