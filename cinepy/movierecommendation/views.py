from django.shortcuts import render
from django.http import HttpResponse
from .db import get_movies_by_search, get_single_movie, get_netflix_movies
from .tmdb_search import TMDB_Metadata
from django.http import HttpResponse
from .likeXbutY import likeXbutY


def home(request):
    query = request.GET.get('query', '') 
    movies = []
    if query:
        movies = get_movies_by_search(query)
    return render(request, 'searchPage.html', {'movies': movies, 'query': query})

def movie_detail(request, movieId):
    movie = get_single_movie(movieId)
    selected_language = request.GET.get('language', 'en')

    matchedMovieIds = likeXbutY(tmdbId=movie['tmdbId'], tmdb_api_key='', originalLanguage=selected_language)

    matchedMovies = get_netflix_movies(matchedMovieIds)

    return render(request, 'movieDetail.html', {'movie': movie, 'matchedFilms': matchedMovieIds, 'matchedMovies': matchedMovies})

    


