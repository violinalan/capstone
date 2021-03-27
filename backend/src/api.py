import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Movie, Actor
from .auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    @TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    # db_drop_and_create_all()

    ## ROUTES
    @app.route('/movies')
    @requires_auth('get:movies')
    def retrieve_movies(payload):
        selection = Movie.query.order_by(Movie.id).all()

        if len(selection) == 0:
            abort(404)

        movies = [movie.long() for movie in selection]
        
        return jsonify({
            'success': True,
            'movies': movies,
        })

    @app.route('/actors')
    @requires_auth('get:actors')
    def retrieve_actors(payload):
        selection = Actor.query.order_by(Actor.id).all()

        if len(selection) == 0:
            abort(404)

        actors = [actor.long() for actor in selection]
        
        return jsonify({
            'success': True,
            'actors': actors,
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movie')
    def create_movie(payload):
        body = request.get_json()

        new_title = body.get('title', None)
        new_year_released = body.get('year_released', None)

        if (not new_title) or (not new_year_released):
            abort(400)

        new_movie = Movie(title=new_title, year_released=new_year_released)
        new_movie.insert()

        movie_list = Movie.query.filter(Movie.title == new_title).all()
        movie = [m.long() for m in movie_list]

        return jsonify({
            'success': True,
            'movies': movie
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actor')
    def create_actor(payload):
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if (not new_name) or (not new_age) or (not new_gender):
            abort(400)

        new_actor = Actor(name=new_name, age=new_age, gender=new_gender)
        new_actor.insert()

        actor_list = Actor.query.filter(Actor.name == new_name).all()
        actor = [a.long() for a in actor_list]

        return jsonify({
            'success': True,
            'actors': actor
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movie(payload, movie_id):
        body = request.get_json()

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        if 'title' in body:
            movie.title = body.get('title')

        if 'year_released' in body:
            movie.year_released = body.get('year_released')

        movie.update()

        movie_list = Movie.query.filter(Movie.id == movie_id).all()
        movie = [m.long() for m in movie_list]

        return jsonify({
            'success': True,
            'movies': movie
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('edit:actor')
    def edit_actor(payload, actor_id):
        body = request.get_json()

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        if 'name' in body:
            actor.name = body.get('name')

        if 'age' in body:
            actor.age = body.get('age')

        if 'gender' in body:
            actor.gender = body.get('gender')

        actor.update()

        actor_list = Actor.query.filter(Actor.id == actor_id).all()
        actor = [a.long() for a in actor_list]

        return jsonify({
            'success': True,
            'actors': actor
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'delete': movie_id,
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'delete': actor_id,
        })

    ## Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 400,
                        "message": "bad request"
                        }), 400

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
                        "success": False, 
                        "error": 401,
                        "message": "unauthorized"
                        }), 401

    return app

app = create_app()

if __name__ == '__main__':
    app.run()