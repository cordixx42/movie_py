'''
Joining MovieLens and WhatsOnNetflix Data
'''

import pandas as pd 
import re
from rapidfuzz import process


pd.set_option('display.max_columns', None)

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
netflixMovies = pd.read_json('whatsOnNetflix_2082025.json')
print(netflixMovies.head(30))

# read movielens 
movieData = pd.read_csv('movielens/movies.csv')
movieData = movieData.dropna()

# extract new column with year out of title, remove year from title 
movieData['year'] = movieData['title'].str.extract(r'\((\d+)\)')
movieData = movieData.drop(movieData[movieData['year'].str.len() < 4].index)


# remove year from title
movieData['title'] = movieData['title'].str.replace(r'\s\(\d+\)', '', regex=True)

# NORMALIZATION MERGE using REGEX
netflixMoviesNorm = netflixMovies.copy()
movieDataNorm = movieData.copy()
netflixMoviesNorm['norm_title'] = netflixMoviesNorm['Title'].apply(normalize_v1)
movieDataNorm['norm_title'] = movieDataNorm['title'].apply(normalize_v1)

# merge on title
# 2333 matches with normalize_v1
merged = pd.merge(netflixMoviesNorm, movieDataNorm, left_on=['norm_title', 'Release Year'], right_on=['norm_title','year'], how='inner')

print(merged.head())
print(merged.describe())

print(merged.head(20))


# FUZZY MERGE using library

netflixMoviesFuzzy = netflixMovies.copy()
movieDataFuzzy = movieData.copy()
# List to store the merged results
merged_results = []

# Set the threshold similarity score
# with threshold 88% 2668 movies matched
threshold = 88


# Loop over each unique year in the netflixMoviesFuzzy dataset
for year in netflixMoviesFuzzy['Release Year'].unique():
    # Filter both datasets for the current year
    subset_netflix = netflixMoviesFuzzy[netflixMoviesFuzzy['Release Year'] == year]
    subset_movie_data = movieDataFuzzy[movieDataFuzzy['year'] == year]

    # List to store matched indices for the current year
    matched_indices = []

    # Perform fuzzy matching only within this subset
    for title1 in subset_netflix['Title']:
        match = process.extractOne(title1, subset_movie_data['title'], score_cutoff=threshold)
        
        # Find the index of the best match, if any
        if match:
            matched_index = subset_movie_data.index[subset_movie_data['title'] == match[0]].tolist()[0]
            matched_indices.append(matched_index)
        else:
            matched_indices.append(None)  # If no match, append None

    # Add the matched indices to the subset
    subset_netflix.loc[:, 'matched_index'] = matched_indices


    subset_netflix['matched_index'] = pd.to_numeric(subset_netflix['matched_index'], errors='coerce')       

    # Merge the dataframes using the matched index (for current year)
    merged_subset = pd.merge(subset_netflix, subset_movie_data, left_on='matched_index', right_index=True, how='left')
    
    # Drop the matched index column as it's no longer needed
    merged_subset = merged_subset.drop(columns=['matched_index'])

    # Append the merged result to the list
    merged_results.append(merged_subset)

# Combine all merged subsets into one dataframe
final_merged_df = pd.concat(merged_results, ignore_index=True)

# Optional: You can check the result of the final merged dataframe
print(final_merged_df.describe())


print(final_merged_df.head(20))




""" matched_indices = []
netflixMoviesFuzzy = netflixMovies.copy()
movieDataFuzzy = movieData.copy()


matched_indices = []

# Set the threshold similarity score
threshold = 93

for title1 in netflixMoviesFuzzy['Title']:
    # Find the best match for each title from df1 in df2's title column
    match = process.extractOne(title1, movieDataFuzzy['title'])

    # Check if the similarity score is above the threshold
    if match[1] >= threshold:
        matched_indices.append(match[2])  # Store the index of the best match
    else:
        matched_indices.append(None)  # If no match, append None

# Add the matched index as a new column to df1
netflixMoviesFuzzy['matched_index'] = matched_indices

# Merge the dataframes using the matched index
merged_df = pd.merge(netflixMoviesFuzzy, movieDataFuzzy, left_on='matched_index', right_index=True, how='left')

# Drop the matched index column as it's no longer needed
merged_df = merged_df.drop(columns=['matched_index'])

print(merged_df.describe()) """