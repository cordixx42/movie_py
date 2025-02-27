# movie_py
Team Mango Rhubarb Lychee Py
Team Name: MaRuLy Py

## Project: CinePy
### Abstract
This project using Selenium to dynamically scrape a site which stores a table of films that are avaialble to watch on netflix. We use a previously downloaded file which is maintained by Movie Lens out of University of Minnesota to add any genre tags to the available films. We also gather movie data for each of the Netlix movies by using an API call to TMDb. This call checks that the film exists and then returns all the summaries/descriptions of each of those films. By using Sentence_transformers, we perform a weighted average of bert embedding based on genres and summaries then store this data in our MongoDB database. Using Django, we created a web-app which allows a user to search for a film and specify a language. With that done, the user will then be provided with movies which are similar to the user's search. 

### Data Sources:
(csv) MovieLens - a large dataset of films with corresponding metadata
(webScraped) whatsOnNetflix.com - Netflix availability and genre information
(api) theMovieDB - source for genres, metadata, and movie-posters
(python) django for web-dev, selenium for web-scraping

### User Instructions
NEEDED: 
- Libraries which must be downloaded (and from where, specify pip or anaconda or whatever)
- Recomended environment (Spyder/Jupyter/VS etc..)
- Which files are needed
- Where files are located
- What commands to be used


### Project One-line Description:
A recommendation app that takes a film [X] and language [Y] as an input and returns a film similar to the input film, but produced in the input language.

### Project Motivation:
It is the ambition of the project team that this app will encourage users to expand their cinematic horizons and cultural literacy by exposing them to films they are likely to enjoy that come from cultural traditions different from their typical media consumption.

### Project Use-Case:
For individuals who enjoy watching movies on Netflix, facilitate finding movies which they might like but are outside of the normal set of films recommended within the USA and thus expand their cinematic-cultural perspective and find something interesting to watch!

### Architecture:
Database of ‘Searchable’ films from movielens
Database of ‘Matchable’ films from whatsonnetflix
Users dynamically search ‘Searchable’ and select a single film denoted x
Users select from a menus features [Y] (unique values available filter criteria in ‘Matchable’), denoted y
Python script calls df.Matchable.iloc[(y in Y):[setGenres]], then calculates a similarity score between filtered x and subset of ‘Matchable’
Returns a recommend film (or films) that are highest ranked in similarity score
Web-interface with django will have dynamic search feature and return film description and poster
mongodb for datastorage

### File explinations
Please call out what each file does here. 

Data Collection
- whats_on_netflix.py - Dynamically scrapes WhatsOnNetflix.com's Library table of all the Netlflix movies available and saves them to a dataframe. 
- tmdb_search.py - takes either a TMDb ID or a film title and searches TMDb via API. If there is a positive result, the data is provided for the film in a dictionary. If not, there is an error expresses as a dicitnary as well. 
- movie_lens.py
- etc...
Data Analysis
- WONanalysis.ipynb - A Jupyter Notebook which shows some simple analysis of the Netflix data. Years, languages, and top performers. 
Recomendation Engine
- likeXbutY.py - Like XbutY matches target film against by a weighted average of bert embedding based on genres and summaries of those films. Filters by language as well.  
Web App
- name of file. 

### code walkthrough
- Process: (MongoDB, Selenium, Requests)
whats_on_netflix - scrape the website and save every netflix movie available. 
then set up TMDB API and search script.
Movie lens loaded into mongoDB, include all tags. 

Matched TMDB to Netlix data, added TMDB data to those movies. and put into another table
Calculate BERT embedding for genre and overview of each movie in TMDB enhanced Netflix table. 

- Recomendation: (Sentence_transformers)
Take a movie lens movie -> get TMDB data -> generate BERT embeddings
We use the TMDB data to get the original language for the movie, and get the 
Compare that data against every movie in the TMDB enhanced Netflix table leading to a list of results. 

- Webapp logic: (Django)
Once the webapp is launched. Navigate to the websight
Select a language which is desired.
Search for a movie which you like. 
The search results will show the most similar movies to what you typed in. 
Select the search which matches what you intended from the table of movies
That will bring you into a list of movies w

# Grading rubric
Source code (40 points), documentation (10 points), user instructions (5 points), abstract (5 points)

