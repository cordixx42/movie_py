# movie_py
Team: Mango Rhubarb Lychee Py

Team Name: MaRuLy Py

## Project: CinePy
### Abstract
A web-based recommendation app that takes a film [X] and a language [Y] as inputs and return a list of films similar to X in the language Y. The set of potential inputs are sourced from MovieLens, a research center at the University of Minnesota, in the form several csv files containing rich metadata and unique identifiers (including tmdb-ids) for 32M films. The set of potential outputs and languages are scraped from whatsOnNetflix.com. Supplementary metadata and genre information for matching are sourced from the TMDB API. After a film is selected by the user, the set of potential outputs is filtered by language then ranked based on a weighted similarity of BERT embeddings on genres and plot summaries. The final results are displayed alongside TMDB-sourced metadata and artifacts for each film. UI is a web-based application built in Django with backend support from a MongoDB database.

### Data Sources:
- (csv) MovieLens - a large dataset of films with corresponding metadata
- (webScraped) whatsOnNetflix.com - Netflix availability and genre information
- (api) theMovieDB - source for genres, metadata, and movie-posters

### Additional Python Packages:
 - Django - web-dev
 - Selenium - web-scraping
 - Sentence_Transformers - BERT embeddings

### User Instructions
Required packages:
 - (requirement.txt) file lists all required packages
 - - to install, run <code>pip install -r /path/to/requirements.txt</code>
Required other software:
 - (MongoDB Community Edition) - to install, run:
 - - install [MongoDB](https://www.mongodb.com/docs/v7.0/administration/install-community/)
Required sub-directories:
 - <code>data_collection</code>,
 - <code>data_analysis</code>, and
 - <code>filtered_matching</code>
Startup Instructions:
 - Initialize database
 - - to start the service, run:
 - - - (appleOS)
 - - to load the data, run: 
 - - - <code>data_collection/load_movielens_mongodb.py</code>
 - - - <code>load_netflix_tmdb_mongodb.py</code>
 - Add TMDB API Key to the files:
 - - in file: <code>movierecommendation/views.py</code>)
 - - - in function: <code>movieDetail</code>
 - Start the webapp:
 - - from <code>cinepy</code>, run <code>python manage.py runserver</code>:
 - Access the webapp:
 - - <code>localhost:8000</code>
 - - Input movie name and target language
 - - Click <Search>
 - - Click desired film's name
 - - Select a new film to watch on Netflix

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

### File Explanations:
Data Collection
- <code>whats_on_netflix.py</code> - Dynamically scrapes WhatsOnNetflix.com's Library table of all the Netlflix movies available and saves them to a dataframe. 
- <code>tmdb_search.py</code> - takes either a TMDb ID or a film title and searches TMDb via API. If there is a positive result, the data is provided for the film in a dictionary. If not, there is an error expressed as a dictionary as well. 
- <code>load_movielens_mongodb.py</code> - A script which loads all Movielens movies with information into a Mongodb collection
- <code>load_netflix_tmdb_mongodb.py</code> - A script which takes all Netflix movies from the WhatsOnNetflix scraped data, adds information using the tmdb API call and loads the movies into another Mongodb collection
Data Analysis
- <code>WONanalysis.ipynb</code> - A Jupyter Notebook which shows some simple analysis of the Netflix data. Years, languages, and top performers. 
Recommendation Engine
- <code>likeXbutY.py</code> - Like XbutY matches target film against by a weighted average of bert embedding based on genres and summaries of those films. Filters by language as well. 
Web App
- <code>cinepy</code> - this directory contains the web app which allows users to select a movie and a target language and get movie recommendations in the target language similar to the selected movie. The <code>movierecommendation/db.py</code> file establishes a connection to the mongodb database and defines functions to query the movielens and netflix movies. The <code>movierecommendation/views.py</code> contains the logic generating the web views, the HTML templates are in <code>movierecommendation/templates/</code>

###Code Walkthrough
- Process: (MongoDB, Selenium, Requests)
whats_on_netflix - scrape the website and save every netflix movie available. 
then set up TMDB API and search script.
Movie lens loaded into mongoDB, include all tags. 

Matched TMDB to Netlix data, added TMDB data to those movies. and put into another table
Calculate BERT embedding for genre and overview of each movie in TMDB enhanced Netflix table. 

- Recommendation: (Sentence_transformers)
Take a movie lens movie -> get TMDB data -> generate BERT embeddings
We use the TMDB data to get the original language for the movie, and get the 
Compare that data against every movie in the TMDB enhanced Netflix table leading to a list of results. 

- Webapp logic: (Django)
Once the webapp is launched. Navigate to the website on <code>localhost:8000</code>
Select a target language you want to watch a movie in.
Search for a movie which you like.
Click on the movie name.
This will redirect you to another page which shows the most similar movies in the target language you selected. 



