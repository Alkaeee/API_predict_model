import json
from flask import Flask, request, jsonify
import sqlite3
import os


def db_connection():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    return cursor

def close_connection(connection):
    connection.close()


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to mi API conected to my books database"

# 0.Ruta para obtener todos los libros
@app.route('/books', methods=['GET'])
def all_books():
    cursor = db_connection()
    query = cursor.execute("SELECT * FROM books")
    books = []
    for b in query:
        books.append(b)
    return jsonify(books)
# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route('/books/count', methods=['GET'])
def count_books():
    cursor = db_connection()
    query = cursor.execute("SELECT author, COUNT(*) AS Count_books FROM books GROUP BY author ORDER BY Count_books DESC")
    books = []
    for b in query:
        books.append(b)
    return jsonify(books)


# 2.Ruta para obtener los libros de un autor como argumento en la llamada
@app.route('/books/author', methods=['GET'])
def author_books():
    author = request.args["author"]
    cursor = db_connection()
    query = cursor.execute(f"SELECT title FROM books WHERE author = '{author}'")
    books = []
    for b in query:
        books.append(b)
    return jsonify(books)

# 3.Ruta para obtener los libros filtrados por título, publicación y autor
@app.route('/books/titlebook', methods=['GET'])
def filter_books():
    title = request.args["title"]
    pub = request.args["published"]
    author = request.args["author"]
    cursor = db_connection()
    query = cursor.execute(f"SELECT * FROM books WHERE author = '{author}' AND title = '{title}' AND published = {pub}")
    books = []
    for b in query:
        books.append(b)
    return jsonify(books)

app.run()