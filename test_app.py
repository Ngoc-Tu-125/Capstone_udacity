import unittest
import json
from app import create_app, setup_db

class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgresql://postgres:120598@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'Enjoy life',
            'release_date': '2022-09-09'
        }

        self.new_actor = {
            'name': 'Tu',
            'age': 25,
            'gender': 'male'
        }

        self.headers = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRNUTFJWVZiVFhYSFRjaU9iWGMtQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1sOGxmc3MxZGU4eHltaWZ5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJqU3lJUmFKb2Ridm9XWW5DOXpZbmFvaGxqQjBhVE9JcUBjbGllbnRzIiwiYXVkIjoiQ2Fwc3RvbmVfdWRhY2l0eSIsImlhdCI6MTY5NjA2MjE1MiwiZXhwIjoxNjk2MTQ4NTUyLCJhenAiOiJqU3lJUmFKb2Ridm9XWW5DOXpZbmFvaGxqQjBhVE9JcSIsInNjb3BlIjoiZ2V0OmFjdG9ycyBnZXQ6bW92aWVzIHBvc3Q6YWN0b3JzIGRlbGV0ZTphY3RvcnMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBkZWxldGU6bW92aWVzIHBvc3Q6bW92aWVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJkZWxldGU6bW92aWVzIiwicG9zdDptb3ZpZXMiXX0.easSkGGr_gGZAq8_WCu3ZPtrohfSlPWSTwpCGQGY76K2PKjA_987YmkJ_UIpLL0y1eAKL9QQd1yR-Qtk5NXrOaoh6DRfM4rbRx1qSCOOGVIgDe9PRJVP7eCULo-vTUORcYWOcfKb_RwbaQ-3_wmLeCTYAa4TDsKaXCUboUP6q_U-KvOMyJtysU7akuwFRTcifZq0VSde-Zl33gNdGVh7V2SNKK9TV5WMyuooa4z4kRmiTyAIA2JGJ-MM2x2JgExWcKD2NyIFYLClmlIjX-fqI8_8TSebLsJFowb9IMHfOt7ucia_1Xx5LsJMhLJP5t4hjBLwXcfZbfFm_ssvismaLg'
        }
    def tearDown(self):
        # Clear any added data to maintain database state
        pass

    # Test get
    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['movies'], list)

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['actors'], list)

    # Test create
    def test_create_actor(self):
        res = self.client().post('/actors', headers=self.headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_create_movie(self):
        res = self.client().post('/movies', headers=self.headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

    # Test error
    def test_400_for_failed_create_actor(self):
        res = self.client().post('/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad request')


    # Test RBAC
    def test_RBAC_create_actor_allowed(self):
        res = self.client().post('/actors', headers=self.headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])

    def test_RBAC_create_actor_not_allowed(self):
        unauthorized_headers = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRNUTFJWVZiVFhYSFRjaU9iWGMtQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1sOGxmc3MxZGU4eHltaWZ5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJqU3lJUmFKb2Ridm9XWW5DOXpZbmFvaGxqQjBhVE9JcUBjbGllbnRzIiwiYXVkIjoiQ2Fwc3RvbmVfdWRhY2l0eSIsImlhdCI6MTY5NjA0NjM4MywiZXhwIjoxNjk2MTMyNzgzLCJhenAiOiJqU3lJUmFKb2Ridm9XWW5DOXpZbmFvaGxqQjBhVE9JcSIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbXX0.VYVS7Ibo4_PW_B-NOpfDdVpZqe8-_lyOIyw8XMx_chQjlYuWjw5iWjtvMTjrQ-l7YrIUJlne6AWtQWUhnR-BzyfcAR8qjzzGL3Kgfsvc5l8IxsfUk6Xb5z2PxpxSiUatvJg080AY2Z-94jPz7jxTYPyAAYCfWBnwnvXZt8G5xspLlU184a8c3r2dUskTWxz606t6AVmPmq1BXP3HQ25rTxcC5HxSxP8erWyW-pz_0uYbLglZBHI7ynzvbaW95YIgaGld0faRQBlXgvyASZksohF43IgXGPL7DSepmAG018F86pfS64lwYtZyoWUCgZAj7kVTZv5QhFYltxg-TVdLJw'
        }

        res = self.client().post('/actors', headers=unauthorized_headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

if __name__ == "__main__":
    unittest.main()
