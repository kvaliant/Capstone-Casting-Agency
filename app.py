import os
from models import setup_db, db, Movie, Actor
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_migrate import Migrate
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  migrate = Migrate(app, db)

  '''
  GET /
  '''
  @app.route('/', methods= ['GET'])
  def login():
    return redirect('https://fsnd21.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=L5gNkzVzN9bJlTLDLuWt9MQChBDCo7Ck&redirect_uri=https://127.0.0.1:8080/login-result')
  
  '''
  GET /actors and /movies 
  '''
  @app.route('/actors', methods = ['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
    actors = Actor.query.all()
    formatted_actors = [actor.format() for actor in actors]
    return jsonify({
      'success': True,
      'actors':formatted_actors
      })

  @app.route('/movies', methods = ['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    movies = Movie.query.all()
    formatted_movies = [movie.format() for movie in movies]
    return jsonify({
      'success':True,
      'movies':formatted_movies
      })

  '''
  POST /actors and /movies 
  '''
  @app.route('/actors', methods = ['POST'])
  @requires_auth('post:actors')
  def post_actor(payload):
    try:
      data = request.get_json()
      name = data["name"]
      age = data["age"]
      gender = data["gender"]
      actor = Actor(name = name, age= age, gender=gender)
      actor.insert()
      formatted_actor = actor.format()
      return jsonify({
        'success': True,
        'actor':formatted_actor
        })
    except:
      abort(422)

  @app.route('/movies', methods = ['POST'])
  @requires_auth('post:movies')
  def post_movie(payload):
    try:
      data = request.get_json()
      title = data["title"]
      release_date = data["release_date"]
      movie = Movie(title = title, release_date= release_date)
      movie.insert()
      formatted_movie = movie.format()
      return jsonify({
        'success': True,
        'movie':formatted_movie
        })
    except:
      abort(422)
  '''
  PATCH /actors and /movies 
  '''
  @app.route('/actors/<int:actor_id>', methods = ['PATCH'])
  @requires_auth('patch:actors')
  def patch_actor(payload, actor_id):
    data = request.get_json()
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)
    try:
      name = data["name"]
      actor.name = name
    except:
      None
    try:
      age = data["age"]
      actor.age = age
    except:
      None
    try:
      gender = data["gender"]
      actor.gender = gender
    except:
      None
    try:
      actor.update()
    except:
      abort(422)
    formatted_actor = actor.format()
    return jsonify({
      'success': True,
      'actor':formatted_actor
      })

  @app.route('/movies/<int:movie_id>', methods = ['PATCH'])
  @requires_auth('patch:movies')
  def patch_movie(payload, movie_id):
    data = request.get_json()
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie == None:
      abort(404)
    try:
      title = data["title"]
      movie.title = title
    except:
      None
    try:
      release_date = data["release_date"]
      movie.release_date = release_date
    except:
      None
    try:
      movie.update()
    except:
      abort(422)
    formatted_movie = movie.format()
    return jsonify({
      'success': True,
      'movie':formatted_movie
      })
  '''
  DELETE /actors and /movies 
  '''
  @app.route('/actors/<int:actor_id>', methods = ['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    data = request.get_json()
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor == None:
      abort(404)
    try:
      actor.delete()
    except:
      abort(422)
    return jsonify({
      'success': True,
      'deleted':1
      })

  @app.route('/movies/<int:movie_id>', methods = ['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
    data = request.get_json()
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie == None:
      abort(404)
    try:
      movie.delete()
    except:
      abort(422)
    return jsonify({
      'success': True,
      'deleted':1
      })

  '''
  Error handler
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422
  
  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
      "success": False, 
      "error": 401,
      "message": "unauthorized"
      }), 401

  @app.errorhandler(405)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405


  @app.errorhandler(AuthError)
  def unauthorized(error):
    return jsonify({
        "success": False, 
        "error": error.status_code,
        "message": error.error.get('description',None)
        }), error.status_code
        
  return app

APP = create_app()


if __name__ == '__main__':
  APP.run(host='0.0.0.0', port=8080, debug=True)

