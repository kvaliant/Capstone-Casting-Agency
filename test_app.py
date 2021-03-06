import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

casting_assistant = os.environ.get('ASSISTANT')
casting_director = os.environ.get('DIRECTOR')
executive_producer = os.environ.get('PRODUCER')

database_path = os.environ.get('DATABASE_URL')
# 'postgres://niflpdzmddyvym:d15bd058036354d888956bdb712df348f9905077991a725b1f3a81da259ac811@ec2-54-211-176-156.compute-1.amazonaws.com:5432/d2ups5itukv3f3'

'''
Tests:
    One test for success behavior of each endpoint
    One test for error behavior of each endpoint
    At least two tests of RBAC for each role
'''


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    Endpoint Test
    '''
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': f'Bearer {executive_producer}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': f'Bearer {executive_producer}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_actor(self):
        res = self.client().post('/actors', headers={'Authorization': f'Bearer {executive_producer}'}, json={"name": "test", "age": 1, "gender": "male"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_post_actor(self):
        res = self.client().post('/actors', headers={'Authorization': f'Bearer {executive_producer}'}, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_post_movie(self):
        res = self.client().post('/movies', headers={'Authorization': f'Bearer {executive_producer}'}, json={"title": "test", "release_date": "2021-11-11"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_post_movie(self):
        res = self.client().post('/movies', headers={'Authorization': f'Bearer {executive_producer}'}, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_patch_actor(self):
        self.actor = Actor(name="test", age=1, gender="male")
        self.actor.insert()
        res = self.client().patch(f'/actors/{self.actor.id}', headers={'Authorization': f'Bearer {executive_producer}'}, json={"name": "test1"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.actor.delete()

    def test_error_patch_actor(self):
        res = self.client().patch('/actors/999', headers={'Authorization': f'Bearer {executive_producer}'}, json={"name": "test1"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_patch_movie(self):
        self.movie = Movie(title="test", release_date="2021-11-11")
        self.movie.insert()
        res = self.client().patch(f'/movies/{self.movie.id}', headers={'Authorization': f'Bearer {executive_producer}'}, json={"title": "test1"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.movie.delete()

    def test_error_patch_movie(self):
        res = self.client().patch('/movies/999', headers={'Authorization': f'Bearer {executive_producer}'}, json={"title": "test1"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_delete_actor(self):
        self.actor = Actor(name="test", age=1, gender="male")
        self.actor.insert()
        res = self.client().delete(f'/actors/{self.actor.id}', headers={'Authorization': f'Bearer {executive_producer}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_delete_actor(self):
        res = self.client().delete('/actors/999', headers={'Authorization': f'Bearer {executive_producer}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_delete_movie(self):
        self.movie = Movie(title="test", release_date="2021-11-11")
        self.movie.insert()
        res = self.client().delete(f'/movies/{self.movie.id}', headers={'Authorization': f'Bearer {executive_producer}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.movie.delete()

    def test_error_delete_movie(self):
        res = self.client().patch('/movies/999', headers={'Authorization': f'Bearer {executive_producer}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    '''
    RBAC Test
    '''
# view actors
    def test_casting_assistant(self):
        res = self.client().get('/actors', headers={'Authorization': f'Bearer {casting_assistant}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# add actor
    def test_error_casting_assistant(self):
        res = self.client().post('/actors', headers={'Authorization': f'Bearer {casting_assistant}'}, json={"name": "test", "age": 1, "gender": "male"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

# add actor
    def test_casting_director(self):
        res = self.client().post('/actors', headers={'Authorization': f'Bearer {casting_director}'}, json={"name": "test", "age": 1, "gender": "male"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# add movie
    def test_error_casting_director(self):
        res = self.client().post('/movies', headers={'Authorization': f'Bearer {casting_director}'}, json={"title": "test", "release_date": "2021-11-11"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

# add movie
    def test_executive_producer(self):
        res = self.client().post('/movies', headers={'Authorization': f'Bearer {executive_producer}'}, json={"title": "test", "release_date": "2021-11-11"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# delete movie
    def test_executive_producer_2(self):
        self.movie = Movie(title="test", release_date="2021-11-11")
        self.movie.insert()
        res = self.client().delete(f'/movies/{self.movie.id}', headers={'Authorization': f'Bearer {executive_producer}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.movie.delete()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
