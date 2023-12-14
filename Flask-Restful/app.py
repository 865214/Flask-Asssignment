from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json
app = Flask(__name__)
api = Api(app)
data_books = [
    {'id' : 1, 'title' : 'Harry Potter'},
    {'id' : 2 , 'title' : 'Snow White'},
    {'id' : 3, 'title' : 'The 2 States'}
]
def find_book(book_id):
    for book in data_books:
        if book['id'] == book_id:
            return book
    return None
        
class Book(Resource):
    def get(self):
        return data_books
    def post(self):
        new_book = {
            'id' : len(data_books) +1,
            'title': 'The witcher'
        }
        data_books.append(new_book)
        return new_book
        
class BookResource(Resource):
    def get(self, book_id):
        book = find_book(book_id)
        if book:
            return book
        return {'Error, Book not found'}
    def put(self, book_id):
        book = find_book(book_id)
        if book:
            book['title'] = request.json['title']
            return book
        return {'Error Message : Book not found'}
    def delete(self, book_id):
        global data_books
        data = [ book for book in data_books if book['id'] != book_id]
        json.dumps(data)
        return {'message : Book deleted Successfully'}
    
api.add_resource(Book, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')

if __name__ == '__main__':
    app.run()