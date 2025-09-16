# นายปวริศ กุลแก้ว 663380019-2 sec.1

from flask import Flask, request
from flask_restful import Resource, Api
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

books_data = [
    {"id":1,"name":"The Russian","type":"fiction"},
    {"id":2,"name":"Just as I Am","type":"non-fiction"},
    {"id":3,"name":"The Vanishing Half","type":"fiction"},
    {"id":4,"name":"The Midnight Library","type":"fiction"},
    {"id":5,"name":"Untamed","type":"non-fiction"},
    {"id":6,"name":"Viscount Who Loved Me","type":"fiction"},
]

class Books(Resource):
    def get(self):
        """ 
        Get a list of all books 
        ---
        responses:
          200:
            description: A list of books
        """
        return books_data, 200

    def post(self):
        """
        Create a new book
        ---
        parameters:
          - in: body
            name: Book
            required: true
            schema: 
                id: Book 
                required:
                    - name 
                properties: 
                    name: 
                        type: string 
                        description: The name of the book 
                    type: 
                        type: string 
                        description: The type of the book
        responses:
            201:
                description: A new book created
            400:
                description: Bad request
        """
        new_id = books_data[-1]['id'] + 1
        data = request.get_json()       # retrieves the JSON data from the request object
        new_book = {'id': new_id, 'name': data['name'], 'type': data['type']}
        books_data.append(new_book)
        return new_book, 201


class BooksByName(Resource):
    def get(self, name):
        """
        Get a book by name
        ---
        parameters:
          - name: name
            in: path
            type: string
            required: true
            description: The name of the book to search
        responses:
          200:
            description: Found a book
          404:
            description: Book not found
        """
        for book in books_data:
            if book['name'] == name:
                return book, 200

        return {'message': 'Book not found'}, 404
    
# Routes 
api.add_resource(Books, '/books')
api.add_resource(BooksByName, '/books/<string:name>')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)