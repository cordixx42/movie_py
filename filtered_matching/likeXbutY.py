#Import Required Packages#
import pandas as pd
import numpy as np
import math as m
import requests
import json
from sentence_transformers import SentenceTransformer
from tmdb_search import TMDB_Metadata 

#Import Required Data#
# dfNtflx = pd.read_json('../data_collection/netflix_data_analysis.json')
dfNtflx = pd.read_json('../data_collection/netflix_tmdb_match.json')
dfALL = pd.read_json('../data_collection/all_movie_data_analysis.json')
genreEmbeddings=pd.read_csv('genreEmbeddings.csv',index_col=0)
overviewEmbeddings=pd.read_csv('overviewEmbeddings.csv',index_col=0)
with open('originalLanguages.json', 'r') as f: originalLanguages = json.load(f)

#Initialize BERT model#
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def likeXbutY(tmdbId,tmdb_api_key,originalLanguage=None,alpha=0.6,N=None,dfALL=dfALL,genreEmbeddings=genreEmbeddings,overviewEmbeddings=overviewEmbeddings,originalLanguages=originalLanguages):
    #Validate tmdbId#
    try: tmbdid = int(tmdbId)
    except: raise TypeError('timbdId not coercible to type INT')
    if tmbdid in sorted(dfALL.tmdbId[dfALL.tmdbId.apply(lambda x: not m.isnan(x))].apply(int)):
        try: tmdbMd = TMDB_Metadata(tmdb_api_key, tmbdid)
        except: raise tmdbIdError('timbdAPI call not successful')
    else:
        raise KeyError('timbdId is not a recognized id value')
    #Validate originalLanguage#
    if (originalLanguage == '') or (originalLanguage is None):
        language = None
    else:
        try: language = str(originalLanguage)
        except: raise TypeError('originalLanguage not coercible to type STR')
        if language in originalLanguages.keys():
            language = language
        else:
            raise KeyError('originalLanguage is not a recognized id value')
    #Validate alpha#
    try: alpha = float(alpha)
    except: raise TypeError('alpha not coercible to type FLOAT')
    if 0.0 <= alpha <= 1.0 :
        alpha = alpha
    else:
        raise ValueError('alpha is out of bounds')
    #Validate N#
    if N is None:
        N = None
    else:
        try: N = int(N)
        except: raise TypeError('N not coercible to type INT')
        if N > 0 :
            N = N
        else:
            raise ValueError('N is out of bounds')
    #Filter on language#
    if language is None:
        genreEmbeddings_filtered=genreEmbeddings
        overviewEmbeddings_filtered=overviewEmbeddings
    else:
        filterIds=[int(id) for id in originalLanguages[language]]
        filteredIndex=[i in filterIds for i in genreEmbeddings.index.to_list()]
        genreEmbeddings_filtered=genreEmbeddings.loc[filteredIndex]
        overviewEmbeddings_filtered=overviewEmbeddings.loc[filteredIndex]
    #Find best matches#
    embeddingGenre = model.encode(f'This film has the following genres: {" ".join(tmdbMd['Genres'])}')
    embeddingOverview = model.encode(tmdbMd['Overview'])
    matchedFilms = genreEmbeddings_filtered.index[np.argsort(alpha*(np.dot(genreEmbeddings_filtered,embeddingGenre)/(np.linalg.norm(genreEmbeddings_filtered, axis=1)*np.linalg.norm(embeddingGenre)))+(1-alpha)*(np.dot(overviewEmbeddings_filtered,embeddingOverview)/(np.linalg.norm(overviewEmbeddings_filtered, axis=1)*np.linalg.norm(embeddingOverview))))[::-1]].to_list()
    #Return ordered results#
    if N is None: return matchedFilms
    else: return matchedFilms[0:N]