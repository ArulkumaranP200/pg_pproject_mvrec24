import mysql.connector
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import pdb
import re

connection = mysql.connector.connect(host='localhost', database='moviesdb', user='root', password='12345')
cursor = connection.cursor(buffered=True)

app= Flask(__name__)

@app.route('/')
def home():
    return render_template("search.html")

@app.route('/search', methods=['POST'])
def recommend():
    
    import mysql.connector
    keyword = request.form['keyword']

    # establish connection to the MySQL database
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
     password="12345",
    database="moviesdb"
    )

    # retrieve the movie data from the database
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT title, genres, actorname,actor2name,director_name FROM movie")

    movies = cursor.fetchall()
    from sklearn.feature_extraction.text import TfidfVectorizer

    # create a TfidfVectorizer object
    tfidf = TfidfVectorizer()

    # create a list of movie titles
    titles = [movie[0] for movie in movies]

    # create a list of movie genres, actors, and directors
    genres = [movie[1] for movie in movies]
    actors = [movie[2] for movie in movies]
    directors = [movie[3] for movie in movies]

    # concatenate the genres, actors, and directors into a single string for each movie
    movie_features = []
    for i in range(len(movies)):
        genre = genres[i] if genres[i] is not None else ""
        actor1 = actors[i] if actors[i] is not None else ""
        actor2 = directors[i] if directors[i] is not None else ""
        movie_features.append(genre + ' ' + actor1 + ' ' + actor2)

    # create the TF-IDF matrix for the movie features
    tfidf_matrix = tfidf.fit_transform(movie_features)
    from sklearn.metrics.pairwise import cosine_similarity

    # define a function to get the most similar movies
    def get_similar_movies(keyword, tfidf_matrix, titles, top_n=250):
    # transform the search keyword using the TF-IDF vectorizer
        keyword_tfidf = tfidf.transform([keyword])
    
    # calculate the cosine similarity between the search keyword and each movie in the database
        cosine_similarities = cosine_similarity(keyword_tfidf, tfidf_matrix).flatten()
    
    # get the indices of the top N most similar movies
        similar_movie_indices = cosine_similarities.argsort()[::-1][:top_n]
    
    # return the titles of the most similar movies
    
        return [titles[i] for i in similar_movie_indices]
    # search for movies similar to "The Dark Knight"
    similar_movies = get_similar_movies(keyword, tfidf_matrix, titles)
    # print the similar movies
    
    result=[]
    final=[]

    for i in range(len(similar_movies)):
        
        cleanString = re.sub('\W+','',similar_movies[i])
        cursor.execute("select * FROM movie WHERE title LIKE '%{}%';".format(cleanString))
        u =  cursor.fetchall()
        result.append((len(u), u))
        #print(result)


    #pdb.set_trace()
    total_count = sum(count for count, _ in result)
    for total_count, rows in result:
        f"Count: {total_count}"
        for row in rows:    
            final.append(row)
    cursor.close()
    return render_template('index.html', result = final)

cursor.close()
connection.close()

if __name__ == '__main__':
    app.run(debug=True)


