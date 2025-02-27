from django.shortcuts import render
from django.http import HttpResponse
from .db import get_movies_by_search

# Create your views here.

from django.http import HttpResponse

def home(request):
    query = request.GET.get('query', '')  # Get the search query from the URL
    movies = []

    if query:
        # If a query is provided, search for movies in the database
        movies = get_movies_by_search(query)
    return render(request, 'searchPagev2.html', {'movies': movies, 'query': query})
    # return HttpResponse('<h1>Welcome to the Homepage!</h1>')
