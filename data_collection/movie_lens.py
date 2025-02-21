'''
Joining MovieLens and WhatsOnNetflix Data
'''

import pandas as pd 
import re

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


#netflix scraped 
netflixMovies = pd.read_json('netflix_scraped/whatsOnNetflix_2082025.json')

print(netflixMovies.head(30))


netflixMovies['Title'] = netflixMovies['Title'].apply(normalize_v1)


# read movielens 
movieData = pd.read_csv('movielens/movies.csv')


movieData = movieData.dropna()

# extract new column with year out of title, remove year from title 
movieData['year'] = movieData['title'].str.extract(r'\((\d+)\)')
movieData = movieData.drop(movieData[movieData['year'].str.len() < 4].index)

# remove year from title
movieData['title'] = movieData['title'].str.replace(r'\s\(\d+\)', '', regex=True)
movieData['title'] = movieData['title'].apply(normalize_v1)


# movieData['year'] = movieData['year'].astype(int)

print(movieData['year'].head())
print(netflixMovies['Release Year'].head())

print(netflixMovies.describe())


# merge on title
merged = pd.merge(netflixMovies, movieData, left_on=['Title', 'Release Year'], right_on=['title','year'], how='inner')

print(merged.head())
print(merged.describe())


