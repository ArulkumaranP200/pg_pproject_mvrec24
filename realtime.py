import imdb
from imdb import IMDbDataAccessError
from time import sleep
import mysql.connector
import pdb
connection = mysql.connector.connect(host='localhost',user='root',password='12345',database='moviesdb')
mycursor = connection.cursor()


def fetch_saved_movie_ids():
    fetched_id=[]
    mycursor.execute('SELECT movies_id from movie where movies_id is not null;')
    id_list = mycursor.fetchall()
    for i in id_list:
        fetched_id.append(i[0])
    return fetched_id


def update_table(i, title, year, rating, director, insert_genre, cast, mycursor):
    #print(i, title)
    mycursor.execute("INSERT INTO movie (movies_id, title, year, imdbscore, director_name, genres, actorname) VALUES(%s,%s,%s,%s,%s,%s,%s)",( i, title, year, rating, director, insert_genre, cast))
    connection.commit()

def fetch_data(search_movie, keyword):
    try:
        if keyword == 'director':
            return search_movie['director'][0]['name']
        elif  keyword == 'cast':
            return search_movie['cast'][0]['name']
        elif keyword == 'genre':
            i =  0
            length = len(search_movie['genre'])
            for i in range(length):
                insert_genre= []
                insert_genre.append(str((search_movie['genre'][int(i)])))
                i = i+1
            return insert_genre
        elif keyword == 'rating':
            if search_movie['rating'] == 'NA':
                return search_movie['rating']
        else:
            return search_movie[keyword]
    except KeyError:
        return "NA"
    

ia = imdb.IMDb(accessSystem='http')

def search(i):
    search_movie = ia.get_movie(i)
    #pdb.set_trace()
    if search_movie != 0:
        title = fetch_data(search_movie, 'title')
        year = fetch_data(search_movie, 'year')
        rating = fetch_data(search_movie, 'rating')
        director = fetch_data(search_movie, 'director')
        genre = fetch_data(search_movie, 'genre')
        cast = fetch_data(search_movie, 'cast')
        print(i, title, year, rating, director, genre, cast)
        
        insert_genre = str(genre)  
        update_table(i,title, year, rating, director, insert_genre, cast, mycursor)
    
num = 99999999

existing_movie_ids = fetch_saved_movie_ids()
#pdb.set_trace()
for i in range(num):
    if i>0:
        if existing_movie_ids.count(i) == 0:
            search(str(i))
            i = i+1
