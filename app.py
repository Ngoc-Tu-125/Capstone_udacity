from flask import Flask, jsonify, request, abort
from models import db, Movie, Actor, setup_db
from auth import requires_auth, AuthError
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200

    # POST endpoint to add an actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        if 'post:actors' not in payload['permissions']:
            raise AuthError({
                'code': 'unauthorized',
                'description': 'Permission not found.'
            }, 403)

        body = request.get_json()

        if not body:
            abort(400)

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if not name or not age or not gender:
            abort(400)

        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 201

    # POST endpoint to add a movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        if 'post:movies' not in payload['permissions']:
            raise AuthError({
                'code': 'unauthorized',
                'description': 'Permission not found.'
            }, 403)

        body = request.get_json()

        if not body:
            abort(400, "Missing request body")

        title = body.get('title')
        release_date = body.get('release_date')

        if not title or not release_date:
            abort(400)

        movie = Movie(title=title, release_date=release_date)
        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 201

    # DELETE endpoint to delete an actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        if 'delete:actors' not in payload['permissions']:
            raise AuthError({
                'code': 'unauthorized',
                'description': 'Permission not found.'
            }, 403)

        actor = Actor.query.get(actor_id)

        if not actor:
            abort(404)

        try:
            actor.delete()

            return jsonify({
                'success': True,
                'delete': actor_id
            }), 200
        except Exception as e:
            db.session.rollback()
            abort(400)  # Bad Request

    # DELETE endpoint to delete a movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        if 'delete:movies' not in payload['permissions']:
            raise AuthError({
                'code': 'unauthorized',
                'description': 'Permission not found.'
            }, 403)

        movie = Movie.query.get(movie_id)

        if not movie:
            abort(404)
        try:
            movie.delete()

            return jsonify({
                'success': True,
                'delete': movie_id
            }), 200
        except Exception as e:
            db.session.rollback()
            abort(400)  # Bad Request

    # PATCH endpoint to update an actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)

        if not actor:
            abort(404)

        body = request.get_json()

        if 'name' in body:
            actor.name = body['name']
        if 'age' in body:
            actor.age = body['age']
        if 'gender' in body:
            actor.gender = body['gender']

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    # PATCH endpoint to update a movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)

        if not movie:
            abort(404)

        body = request.get_json()

        if 'title' in body:
            movie.title = body['title']
        if 'release_date' in body:
            movie.release_date = body['release_date']

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    if test_config:
        app.config.update(test_config)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
