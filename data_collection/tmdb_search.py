'''
Script which can get movie data off of TMDB
Not putting API Key in here since this is a public repo. 
'''
import requests

def TMDB_Metadata(key, title, method=1):
    base = 'https://api.themoviedb.org/3'
    if method == 1:
        movie_details = f'{base}/movie/{str(title)}'
        details_param = {'api_key': key}
        # continue to get the movie details - check if actually got something from the API
        details_response = requests.get(movie_details, params=details_param)
        if details_response.status_code == 200:
            metadata = details_response.json()
            return{
                'Title': metadata.get('title'),
                'Original Title': metadata.get('original_title'),
                'Release': metadata.get('release_date'),
                'Overview': metadata.get('overview'),
                'Genres':[genre['name'] for genre in metadata.get('genres', [])],
                'TMDB Rating':metadata.get('vote_average'),
                'TMDB Votes': metadata.get('votes_count'),
                'Poster':metadata.get('poster_path'),
                'Backdrop': metadata.get('backdrop_path'),
                'Adult': metadata.get('adult'),
                'Budget': metadata.get('budget'),
                'TMDB Homepage':metadata.get('homepage'),
                'ID': metadata.get('id'),
                'IMDB ID': metadata.get('imdb_id'),
                'Origingal Language': metadata.get('original_language'),
                'Popularity': metadata.get('popularity'),
                'Production Companies': [company['name'] for company in metadata.get('production_companies', [])],
                'Production Countries': [country['name'] for country in metadata.get('production_countries', [])],
                'Revenue': metadata.get('status'),
                'Runtime': metadata.get('runtime'),
                'Spoken Languages': [language['name'] for language in metadata.get('spoken_languages', [])],
                'Status': metadata.get('status'),
                'Tagline': metadata.get('tagline'), 
                'Video': metadata.get('video')
            }
        else:
            return{'Error': 'Failed to get movie details'}
    else:
        
        seach = f'{base}/search/movie'
        param = {'api_key':key, 'query':title}

        response = requests.get(seach, param)
        # check TMDB for movie based on title - get ID, and url for the details. 
        if response.status_code==200:
            results = response.json().get('results')
            if results:
                movie_id = results[0].get('id')
                movie_details = f'{base}/movie/{movie_id}'
                details_param = {'api_key': key}
                # continue to get the movie details - check if actually got something from the API
                details_response = requests.get(movie_details, params=details_param)
                if details_response.status_code == 200:
                    metadata = details_response.json()
                    return{
                        'Title': metadata.get('title'),
                        'Original Title': metadata.get('original_title'),
                        'Release': metadata.get('release_date'),
                        'Overview': metadata.get('overview'),
                        'Genres':[genre['name'] for genre in metadata.get('genres', [])],
                        'TMDB Rating':metadata.get('vote_average'),
                        'TMDB Votes': metadata.get('votes_count'),
                        'Poster':metadata.get('poster_path'),
                        'Backdrop': metadata.get('backdrop_path'),
                        'Adult': metadata.get('adult'),
                        'Budget': metadata.get('budget'),
                        'TMDB Homepage':metadata.get('homepage'),
                        'ID': metadata.get('id'),
                        'IMDB ID': metadata.get('imdb_id'),
                        'Origingal Language': metadata.get('original_language'),
                        'Popularity': metadata.get('popularity'),
                        'Production Companies': [company['name'] for company in metadata.get('production_companies', [])],
                        'Production Countries': [country['name'] for country in metadata.get('production_countries', [])],
                        'Revenue': metadata.get('status'),
                        'Runtime': metadata.get('runtime'),
                        'Spoken Languages': [language['name'] for language in metadata.get('spoken_languages', [])],
                        'Status': metadata.get('status'),
                        'Tagline': metadata.get('tagline'), 
                        'Video': metadata.get('video')
                    }
                else:
                    return{'Error': 'Failed to get movie details'}
            else:
                return{'Error': 'Movie not found'}
        else:
            return{'Error': 'Search Failed'}
def test():
    movie = 'Fight Club'
    metadata = TMDB_Metadata('API KEY', movie, 0)
    print(metadata)
    movie = 550
    metadata = TMDB_Metadata('API KEY', movie)
    print(metadata)
test()

