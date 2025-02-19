import pandas as pd 
from init_neo import *
from itertools import pairwise
import numpy as np 

# add movies, genres, and years 
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "12345678")



pd.set_option('display.max_columns', None)

movieData = pd.read_csv('movielens/movies.csv')

# extract new column with year out of title, remove year from title 
movieData['year'] = movieData['title'].str.extract(r'\((\d+)\)')

print(movieData.describe())

# remove na rows and not existing  years 
# todo remove years < 1950 and > 2025
movieData = movieData.dropna()
movieData = movieData.drop(movieData[movieData['year'].str.len() < 4].index)
movieData['year'] = movieData['year'].astype(int)

# drop some too old or too recent movies 
movieData = movieData.drop(movieData[movieData['year'] < 1900].index)
movieData = movieData.drop(movieData[movieData['year'] > 2000].index)

# drop movies with no genre listed ?? rethink
movieData = movieData.drop(movieData[movieData['genres'] == "(no genres listed)"].index)

# remove year from title
movieData['title'] = movieData['title'].str.replace(r'\s\(\d+\)', '', regex=True)


print(movieData.describe())



### STARTING WITH NEO4J LOADING
driver = getDriver()

""" 
 # add YEAR nodes 
allYears = set(movieData['year'].drop_duplicates())
for y in allYears:
    addYear(driver,y)

# add YEAR connection 
allYears = list(allYears)
allYears.sort()

print(type(allYears))

for i,j in pairwise(allYears):
    addYearYearRelation(driver,i,j)


# add GENRES 
genreSet = {'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 
            'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
            'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'}

for g in genreSet:
    addGenre(driver,g)


print(movieData.head())

# add MOVIES with their connections to years and genres 
for index, row in movieData.iterrows():
    addMovie(driver, row['title'], row['movieId'])
    addMovieYearRelation(driver, row['title'], row['year'])
    sepGenreList = movieData.loc[index]['genres'].split(sep='|')
    for g in sepGenreList:
        addMovieGenreRelation(driver, row['title'], g)

"""

for index, row in movieData.iterrows():
    #addMovie(driver, row['title'], row['movieId'])
    addMovieYearRelation(driver, row['movieId'], row['year'])
    sepGenreList = movieData.loc[index]['genres'].split(sep='|')
    for g in sepGenreList:
        addMovieGenreRelation(driver, row['movieId'], g)


# TAG PROCESSING 
tagData = pd.read_csv('movielens/tags.csv')
print(tagData.describe())
#drop tags for movies not in our movie set
tagData = tagData.drop(tagData[~tagData['movieId'].isin(movieData['movieId'])].index)
#convert all tags to lower case 
tolower = lambda s: str(s).lower()
tagData['tag'] = tagData['tag'].apply(tolower)
#group by tag name 
tagData = tagData.groupby(['movieId', 'tag'])['userId'].nunique().reset_index(name='user_count')
tagData = tagData.sort_values(by='user_count', ascending=False)
print(tagData.head(10000))
tagData = tagData.head(10000)
#user_count invert it so in graph search less means closer 
min_orig = tagData.describe().loc['min', 'user_count']
max_orig = tagData.describe().loc['max', 'user_count']
minMaxNorm = lambda x, min_orig=min_orig, max_orig=max_orig, min_new=1, max_new=100: ((max_orig - x) / (max_orig - min_orig)) * (max_new - min_new) + min_new


def transform_and_map(value, min_old=8, max_old=603, min_new=1, max_new=100):
    # Apply log transformation to compress the range
    transformed_value = np.log(value - min_old + 1)  # Log transformation
    
    # Apply the normalization to map it to the new range, flipping the range order
    log_min = np.log(min_old - min_old + 1)  # Log of the minimum value
    log_max = np.log(max_old - min_old + 1)  # Log of the maximum value
    
    # Reverse the mapping (so larger values map to lower numbers)
    normalized_value = max_new - ((transformed_value - log_min) / (log_max - log_min) * (max_new - min_new))
    
    return normalized_value


tagData['user_count_inverted'] = tagData['user_count'].apply(transform_and_map)

print(tagData.head())


#create TAGS
""" tags = tagData['tag'].drop_duplicates()
for t in tags:
    addTag(driver, t) """


#create TAG MOVIE relation 
#for index, row in tagData.iterrows():
#    addMovieTagWeightRelation(driver, row['movieId'], row['tag'], row['user_count_inverted'])
