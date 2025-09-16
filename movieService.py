from flask import Flask, request
from flask_restful import Resource, Api
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

MoviePortal = [
    {
        "playlist_id": 1,
        "playlist_name": "datenight",
        "movie_list": [
            "The Notebook",
            "50 First Dates",
            "A Walk to Remember"
        ]
    },
    {
        "playlist_id": 2,
        "playlist_name": "action",
        "movie_list": [
            "Die Hard",
            "Mad Max: Fury Road",
            "John Wick"
        ]
    },
    {
        "playlist_id": 3,
        "playlist_name": "comedy",
        "movie_list": [
            "Superbad",
            "Step Brothers",
            "The Hangover"
        ]
    },
]


class Playlists(Resource):
    def get(self):
        """
        Get a list of all playlists
        ---
        responses:
          200:
            description: A list of all playlists
        """
        return MoviePortal, 200

    def post(self):
        """
        Add a new playlist
        ---
        parameters:
          - in: body
            name: Playlist
            required: true
            schema:
                id: Playlist
                required:
                    - playlist_name
                    - movie_list
                properties:
                    playlist_name:
                        type: string
                        description: The name of the playlist
                    movie_list:
                        type: array
                        items:
                          type: string
                        description: A list of movie titles
        responses:
            201:
                description: A new playlist created
            400:
                description: Bad request (missing/invalid payload)
        """
        data = request.get_json(silent=True) or {}
        # Basic validation
        if 'playlist_name' not in data or 'movie_list' not in data:
            return {"message": "playlist_name and movie_list are required"}, 400
        if not isinstance(data['movie_list'], list):
            return {"message": "movie_list must be a JSON array of strings"}, 400

        # create new id
        if len(MoviePortal) == 0:
            new_id = 1
        else:
            new_id = MoviePortal[-1]['playlist_id'] + 1

        new_playlist = {
            "playlist_id": new_id,
            "playlist_name": data['playlist_name'],
            "movie_list": data['movie_list']
        }
        MoviePortal.append(new_playlist)
        return new_playlist, 201

# Routes
api.add_resource(Playlists, '/playlists')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
