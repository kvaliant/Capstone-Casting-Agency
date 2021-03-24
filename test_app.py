import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

casting_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpZnRiT0xSRm5xOERGMmVrWExUaCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQyMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1YjI2OTA0NGI2OWYwMDcwZGMwMGU3IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTY1ODY5NDQsImV4cCI6MTYxNjY3MzM0NCwiYXpwIjoiTDVnTmt6VnpOOWJKbFRMREx1V3Q5TVFDaEJEQ283Q2siLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.BK0rJ8yjnkPR3zNcKpawD3P3R6uVlUmHTuaI81s_ws4XCdWXGGOINbIt0tAWzPOOu19o_6EMPP3dyatw_yAiuEWbOYzf60cJu3zNr8ekVAypTHnLH4cxr3Oj_6_fthVecnxReIYOonbs3nM1WJueXwzdeJF_Y92y5vRRSILQjMJ94VoO560RY-0loXnRBb86AutG_Fgd5942AuBGMCT0Of3yRdtXYzDknbu0AUfO4PaBnopHczZ_Ib71r2JYVqHFgfvzFy4vlDiRBecyt6JNJcM7LipcRvGDiF9Uymf0ILwLu8VC0Z906IXmTqIZoi1uaqV-gvKxACkKX60UBuesfw'
casting_director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpZnRiT0xSRm5xOERGMmVrWExUaCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQyMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1YjI2OTA0NGI2OWYwMDcwZGMwMGU3IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTY1ODY5NDQsImV4cCI6MTYxNjY3MzM0NCwiYXpwIjoiTDVnTmt6VnpOOWJKbFRMREx1V3Q5TVFDaEJEQ283Q2siLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.BK0rJ8yjnkPR3zNcKpawD3P3R6uVlUmHTuaI81s_ws4XCdWXGGOINbIt0tAWzPOOu19o_6EMPP3dyatw_yAiuEWbOYzf60cJu3zNr8ekVAypTHnLH4cxr3Oj_6_fthVecnxReIYOonbs3nM1WJueXwzdeJF_Y92y5vRRSILQjMJ94VoO560RY-0loXnRBb86AutG_Fgd5942AuBGMCT0Of3yRdtXYzDknbu0AUfO4PaBnopHczZ_Ib71r2JYVqHFgfvzFy4vlDiRBecyt6JNJcM7LipcRvGDiF9Uymf0ILwLu8VC0Z906IXmTqIZoi1uaqV-gvKxACkKX60UBuesfw'
executive_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpZnRiT0xSRm5xOERGMmVrWExUaCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQyMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1YjI2OTA0NGI2OWYwMDcwZGMwMGU3IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTY1ODY5NDQsImV4cCI6MTYxNjY3MzM0NCwiYXpwIjoiTDVnTmt6VnpOOWJKbFRMREx1V3Q5TVFDaEJEQ283Q2siLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.BK0rJ8yjnkPR3zNcKpawD3P3R6uVlUmHTuaI81s_ws4XCdWXGGOINbIt0tAWzPOOu19o_6EMPP3dyatw_yAiuEWbOYzf60cJu3zNr8ekVAypTHnLH4cxr3Oj_6_fthVecnxReIYOonbs3nM1WJueXwzdeJF_Y92y5vRRSILQjMJ94VoO560RY-0loXnRBb86AutG_Fgd5942AuBGMCT0Of3yRdtXYzDknbu0AUfO4PaBnopHczZ_Ib71r2JYVqHFgfvzFy4vlDiRBecyt6JNJcM7LipcRvGDiF9Uymf0ILwLu8VC0Z906IXmTqIZoi1uaqV-gvKxACkKX60UBuesfw'

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
        self.database_name = "capstone"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','admin','localhost:5432', self.database_name)
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
        res = self.client().get('/actors',headers={'Authorization':f'Bearer {executive_producer}'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies(self):
        res = self.client().get('/movies',headers={'Authorization':f'Bearer {executive_producer}'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_actor(self):
        res = self.client().post('/actors',headers={'Authorization':f'Bearer {executive_producer}'},json={"name":"test","age":1,"gender":"male"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_post_actor(self):
        res = self.client().post('/actors',headers={'Authorization':f'Bearer {executive_producer}'},json={})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_post_movie(self):
        res = self.client().post('/movies',headers={'Authorization':f'Bearer {executive_producer}'},json={"title":"test","release_date": "2021-11-11"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_post_movie(self):
        res = self.client().post('/movies',headers={'Authorization':f'Bearer {executive_producer}'},json={})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_patch_actor(self):
        self.actor = Actor(name="test",age=1,gender="male")
        self.actor.insert()
        res = self.client().patch(f'/actors/{self.actor.id}',headers={'Authorization':f'Bearer {executive_producer}'},json={"name":"test1"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.actor.delete()
    
    def test_error_patch_actor(self):
        res = self.client().patch('/actors/999',headers={'Authorization':f'Bearer {executive_producer}'},json={"name":"test1"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_patch_movie(self):
        self.movie = Movie(title="test",release_date="2021-11-11")
        self.movie.insert()
        res = self.client().patch(f'/movies/{self.movie.id}',headers={'Authorization':f'Bearer {executive_producer}'},json={"title":"test1"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.movie.delete()
    
    def test_error_patch_movie(self):
        res = self.client().patch('/movies/999',headers={'Authorization':f'Bearer {executive_producer}'},json={"title":"test1"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_delete_actor(self):
        self.actor = Actor(name="test",age=1,gender="male")
        self.actor.insert()
        res = self.client().delete(f'/actors/{self.actor.id}',headers={'Authorization':f'Bearer {executive_producer}'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_delete_actor(self):
        res = self.client().delete('/actors/999',headers={'Authorization':f'Bearer {executive_producer}'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_delete_movie(self):
        self.movie = Movie(title="test",release_date="2021-11-11")
        self.movie.insert()
        res = self.client().delete(f'/movies/{self.movie.id}',headers={'Authorization':f'Bearer {executive_producer}'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.movie.delete()
    
    def test_error_delete_movie(self):
        res = self.client().patch('/movies/999',headers={'Authorization':f'Bearer {executive_producer}'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    '''
    RBAC Test
    '''
    #view actors
    def test_casting_assistant(self):
        res = self.client().get('/actors',headers={'Authorization':f'Bearer {casting_assistant}'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #add actor
    def test_error_casting_assistant(self):
        res = self.client().post('/actors',headers={'Authorization':f'Bearer {casting_assistant}'},json={"name":"test","age":1,"gender":"male"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    
    #add actor
    def test_casting_director(self):
        res = self.client().post('/actors',headers={'Authorization':f'Bearer {casting_director}'},json={"name":"test","age":1,"gender":"male"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #add movie
    def test_error_casting_director(self):
        res = self.client().post('/movies',headers={'Authorization':f'Bearer {casting_director}'},json={"title":"test","release_date": "2021-11-11"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    #add movie
    def test_executive_producer(self):
        res = self.client().post('/movies',headers={'Authorization':f'Bearer {executive_producer}'},json={"title":"test","release_date": "2021-11-11"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #delete movie
    def test_executive_producer_2(self):
        self.movie = Movie(title="test",release_date="2021-11-11")
        self.movie.insert()
        res = self.client().delete(f'/movies/{self.movie.id}',headers={'Authorization':f'Bearer {executive_producer}'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.movie.delete()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()