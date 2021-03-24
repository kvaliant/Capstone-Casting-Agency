import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

casting_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpZnRiT0xSRm5xOERGMmVrWExUaCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQyMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1YjI2MmU0OTliYTAwMDZhN2M3NjE1IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTY1OTM4MDksImV4cCI6MTYxNjY4MDIwOSwiYXpwIjoiTDVnTmt6VnpOOWJKbFRMREx1V3Q5TVFDaEJEQ283Q2siLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.M4YV-kL1Yr87EC0j30iSAyB-V0ENJWizX0Po9Oqslwa20odkWOsMAFOxSS-XIwGCeI_Nc4wnqB0Fqh5C2oHe8sAcOmUSHJpYHiOdA-M_ARS6mkz8kyRIBjW4rPzRvQatajxD2KBPdNe8N1zrHYFYQQcsumq0tvWvOA30oQi7gRbBsviMj5p9EZZmSuWNwwhTDmOEPpVkgElRhNzaewBcXWnQm6QwlDS8d7SstRBUeBOcv7KZHN529kyjaBRXl-cNfRAI4vy-So-Xleix4phQRhpGYKQjQyUpro1FzYqxits_o1Gvfl-7amrSFqgXcVM2i3oyrhXIIIOe1ETn3DjWlQ'
casting_director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpZnRiT0xSRm5xOERGMmVrWExUaCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQyMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1YjI2Njg5NDA1NTkwMDY5MjBlYTIwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTY1OTM4OTAsImV4cCI6MTYxNjY4MDI5MCwiYXpwIjoiTDVnTmt6VnpOOWJKbFRMREx1V3Q5TVFDaEJEQ283Q2siLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.ePajsX7q2P14cU-uwfNFmsDWOoxAv6QCBy__QHH8yadjecKHAkAP2GPlhzHp1V62ppXLLUfYx06QPtsI2hhB1ptFt3BW0gZqHYlntTadB-sXYF716k6w7x9xus8TdeoaHifNAimbvkCQQb0EcuXM7wGgWlzeKZJ2kIZfP35BA_TL4kQUWk2IGqId_jWKGlCc3omDl4M1T5sjonMxa-x1BxXT6lpbALBEAqzOIDWsFtb6pE79mJjQV2eX9ZagZCfRnyLQ4rVQ5BuX3lsMSpgSKSu6qugeNcwbU_vif09IQP5t9gAnZlIf232QJCHs5CnzELbyeezKpQcI26plzXVS8A'
executive_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVpZnRiT0xSRm5xOERGMmVrWExUaCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQyMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1YjI2OTA0NGI2OWYwMDcwZGMwMGU3IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTY1OTM5MjYsImV4cCI6MTYxNjY4MDMyNiwiYXpwIjoiTDVnTmt6VnpOOWJKbFRMREx1V3Q5TVFDaEJEQ283Q2siLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.kpSmTvNPO8904Shplwaa_C0QUMkmsOliEsfySj3Mu8fZmCJ6wNMH0dZt8o-v_cYjnTaxZ8uhZMAKFT6Y6pDhA2sjEHL9wwKdYpVgPMFTAa4DleiXadbsI04DU0tTLnGqW-jL6bnykRJZX5jHtM-VEULmtko4HI41WKSuj2f74V7iJYfurzP4H5YvM6XSanZrJoSsbCefbgIQb0sZ7S2m7sV8hTifV-Yg91w5OkkNLScIem3evX2B0cDTaj4YpjGLQxkoAMDXmG98JeIvyuGsQoSQsQrGRsMBYoS5Qk48PGPT8wvp6Naaa05MF9oQVTCyMvAUrMtWJ5cmeFxiIQUx5A'

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
        
        self.assertEqual(res.status_code, 200)
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