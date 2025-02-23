from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "12345678")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

def getDriver():
    return GraphDatabase.driver(URI, auth=AUTH)

def addMovie(driver, name, id):
    driver.execute_query(
        "CREATE (n:Movie {movieName: $name, movieId: $id})", 
        name = name,
        id = id,
        database_="neo4j"
    )

def addTag(driver, name):
    driver.execute_query(
        "CREATE (n:Tag {tagDescription: $name})", 
        name = name,
        database_="neo4j"
    )

def addYear(driver, name):
    driver.execute_query(
        "CREATE (n:Year {year: $name})", 
        name = name,
        database_="neo4j"
    )


def addGenre(driver, name):
    driver.execute_query(
        "CREATE (n:Genre {genreName: $name})", 
        name = name,
        database_="neo4j"
    )



def addMovieYearRelation(driver, i, y):
     driver.execute_query(
        """
        MATCH (m:Movie {movieId: $i}), (y:Year {year: $y}) 
        CREATE (m)-[:RELEASED_IN]->(y);
        """, 
        i = i,
        y = y,
        database_="neo4j"
    )
     
def addMovieGenreRelation(driver, i, g):
     driver.execute_query(
        """
        MATCH (m:Movie {movieId: $i}), (g:Genre {genreName: $g}) 
        CREATE (m)-[:BELONGS_TO]->(g);
        """, 
        i = i,
        g = g,
        database_="neo4j"
    )

def addMovieTagRelation(driver, i, t):
    driver.execute_query(
        """
        MATCH (m:Movie {movieId:$i}) 
        WITH m
        MATCH (t:Tag {tagDescription: $t})
        CREATE (m)-[:TAGGED_WITH]->(t);
        """, 
        i = i,
        t = t,
        database_="neo4j"
)
    


def addNetflixNode(driver):
    driver.execute_query(
        "CREATE (n:Netflix {name: 'Netflix'})", 
        database_="neo4j"
)
    

def addMovieNetflixRelation(driver, i):
      driver.execute_query(
        """
        MATCH (m:Movie {movieId: $i}), (n:Netflix {name: 'Netflix'}) 
        CREATE (m)-[:IS_ON]->(n);
        """, 
        i = i,
        database_="neo4j"
    )
      
def addLanguageNode(driver, l):
    driver.execute_query(
        "CREATE (n:Language {name: $l})", 
        l = l,
        database_="neo4j"
)
    
def addMovieLanguageRelation(driver, i, l):
    driver.execute_query(
        """
        MATCH (m:Movie {movieId: $i}), (l:Language {name: $l}) 
        CREATE (m)-[:SPOKEN_IN]->(l);
        """, 
        i = i,
        l = l,
        database_="neo4j"
)

    
# stretch 
def addMovieTagWeightRelation(driver, i, t, w):
    driver.execute_query(
        """
        MATCH (m:Movie {movieId:$i}) 
        WITH m
        MATCH (t:Tag {name: $t})
        CREATE (m)-[:TAGGED_WITH {weight: $w}]->(t);
        """, 
        i = i,
        t = t,
        w = float(w),
        database_="neo4j"
)

