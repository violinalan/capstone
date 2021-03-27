import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRmTnY1WTltRjJNZEhZRjREWXNwLSJ9.eyJpc3MiOiJodHRwczovL2FsYW5zY290dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNzM3YWNmYjM3ZDAwMDY4MjYwYTM3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNjc3MjYxNiwiZXhwIjoxNjE2ODU5MDE2LCJhenAiOiJDdDRQSUI3MERBQ0kzUzdUSXpMc2JLUU15VDdnMTFiRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.TIkkUq262lXZPPPYktsS89iXc1XzlfdiqtJcmEN64Ox7gkdmGBcRaSqE3yVVyDjmp4W1yZumlDjt3WmuPkDS1Kc17FOd5MJnz3gmhbQ7gPpi0HWnZtBAHOiP-Z_wtIBUqknZCyPexxOOQeSnH1FRwPUco0bYKk5JyZbKftnc4bLpAinklZIZp_47EFTHO2DkezvKRRsULCVJZc8Z3u_E8T0uBXmsSCSZpZaX3mZ7ZvCIUElzcLDkCD0_dbS3jhWuW1HjOu6PCpgjUz9P_gjM5RFP8yX6SuzO9LFAj4saXja8N8pmJu1BkPz19PHWwF8VPHsVWQgbDVH1U0jj8dJ-cA"
CASTING_DIRECTOR_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRmTnY1WTltRjJNZEhZRjREWXNwLSJ9.eyJpc3MiOiJodHRwczovL2FsYW5zY290dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNzM3NDQ5ZDgxMWYwMDY5NmNhMTRmIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNjc3MzE1MywiZXhwIjoxNjE2ODU5NTUzLCJhenAiOiJDdDRQSUI3MERBQ0kzUzdUSXpMc2JLUU15VDdnMTFiRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9yIiwiZGVsZXRlOmFjdG9yIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.qNdH4xMwWjFJ7UGSkdQUv3vqsOSsFTo7sqJga3vaAZsn3wVRG55tnmUMb92iloH8fGsQygR1VWZD_dS3pxc_WyLf1E5xz3sbvAOLVpyS_i9xjroyEgw6g9jCkyI263rxtj1DZJQTTqGPsy8uDKGMxSJDozX5TmQZNvrkmJG-cACsPNqiihd3B6fp4ahZylLyK124grHJBOBTNxHpyEXphuc94A6ZbRGsIy6NQuWUt_JM_hQH71g2DwffwsAVqU4JCBDXiYWQ07nE7darH-TQJKkodKTiT8pHZV1pZeLlByZZZ1I1FlShS7803dwSGJkLa76qEt6pDLGjFx4Ur_JZ4w"
EXECUTIVE_PRODUCER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRmTnY1WTltRjJNZEhZRjREWXNwLSJ9.eyJpc3MiOiJodHRwczovL2FsYW5zY290dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyYjYxMDZkYTNmYTIwMDZhYzlkYjQ2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNjc3MzIxMCwiZXhwIjoxNjE2ODU5NjEwLCJhenAiOiJDdDRQSUI3MERBQ0kzUzdUSXpMc2JLUU15VDdnMTFiRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9yIiwiY3JlYXRlOm1vdmllIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.AgUNXbWOLu8_SwdDkZTMacsq3H5CDTg-AR4HEXkYB0QE1NLu0PyX4a0JTURDV7XYaYW4nPqY6fxG_2ncqyBuut-ijfveDJMiTWuxYL4FxTixEq_glK9gGAat8Idl2VYvNOMfjp6J_JevXhaisr2rIV0YX1fF6923YXtR8o803yy9JYz1MhxDno2W8m_hn3OK0xz_wPZaCnGOhjIkA3lItu0n7qmha2yUzsaLkwNv0UmvCpoB1vq3Hl1tYKGyrl4YOsISf0UxPIa0vrWn-WzUWQrcBWJj4DPmDsJpt_YNbdVH6qODoBnHW-hJPJfY98XsD7kwwjtCh6yS03u1KdDQrQ"

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format('alan:vocisuj3@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_movie = {
            "title": "Avengers: Endgame",
            "year_released": 2019
        }

        self.new_movie_bad_request = {
            "title": "Avengers: Endgame2",
        }

        self.new_actor = {
            "name": "Paul Rudd",
            "age": 51,
            "gender": "Male"
        }

        self.new_actor_bad_request = {
            "name": "Paul Rudd",
            "age": 51
        }

        self.new_movie_to_edit = {
            "title": "Black Widow",
            "year_released": 1111
        }

        self.edit_movie = {
            "year_released": 2222
        }

        self.new_actor_to_edit = {
            "name": "Scarlett Johansson",
            "age": 36,
            "gender": "Female"
        }

        self.edit_actor = {
            "gender": "abcde"
        }

        self.new_movie_to_delete = {
            "title": "Captain Marvel",
            "year_released": 1900
        }

        self.new_actor_to_delete = {
            "name": "Chris Evans",
            "age": 39,
            "gender": "Male"
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_401_get_movies_without_auth_header(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')
    
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_401_get_actors_with_empty_bearer_token(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer {}'.format('')})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

        ### Create Movie

    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_create_new_movie_bad_request(self):
        res = self.client().post('/movies', json=self.new_movie_bad_request, headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_create_new_movie_unauthorized(self):
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

        #### Create Actor

    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_create_new_actor_bad_request(self):
        res = self.client().post('/actors', json=self.new_actor_bad_request, headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_create_new_actor_unauthorized(self):
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')


        #### Edit Movie

    def test_edit_movie(self):
        res = self.client().post('/movies', json=self.new_movie_to_edit, headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)

        id_to_edit = data['movies'][0]['id']

        res = self.client().patch('/movies/{}'.format(id_to_edit), json=self.edit_movie, headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)
        self.assertEqual(data['movies'][0]['year_released'], 2222)

    def test_edit_movie_unauthorized(self):
        res = self.client().patch('/movies/999', json=self.edit_movie, headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_edit_movie_that_doesnt_exist(self):
        res = self.client().patch('/movies/999', json=self.edit_movie, headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

        #### Edit Actor

    def test_edit_actor(self):
        res = self.client().post('/actors', json=self.new_actor_to_edit, headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        id_to_edit = data['actors'][0]['id']

        res = self.client().patch('/actors/{}'.format(id_to_edit), json=self.edit_actor, headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)
        self.assertEqual(data['actors'][0]['gender'], 'abcde')

    def test_edit_actor_unauthorized(self):
        res = self.client().patch('/actors/999', json=self.edit_actor, headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_edit_actor_that_doesnt_exist(self):
        res = self.client().patch('/actors/999', json=self.edit_actor, headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

        #### Delete Movie

    def test_delete_movie(self):
        res = self.client().post('/movies', json=self.new_movie_to_delete, headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)

        id_to_delete = data['movies'][0]['id']

        res = self.client().delete('/movies/{}'.format(id_to_delete), headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], id_to_delete)

    def test_delete_movie_unauthorized(self):
        res = self.client().delete('/movies/888', headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_delete_movie_that_doesnt_exist(self):
        res = self.client().delete('/movies/888', headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

        #### Delete Actor

    def test_delete_actor(self):
        res = self.client().post('/actors', json=self.new_actor_to_delete, headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)

        id_to_delete = data['actors'][0]['id']

        res = self.client().delete('/actors/{}'.format(id_to_delete), headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], id_to_delete)

    def test_delete_actor_unauthorized(self):
        res = self.client().delete('/actors/888', headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_delete_actor_that_doesnt_exist(self):
        res = self.client().delete('/actors/888', headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()