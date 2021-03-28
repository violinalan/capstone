import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from database.models import setup_db, Movie, Actor

CASTING_ASSISTANT_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRmTnY1WTltRjJNZEhZRjREWXNwLSJ9.eyJpc3MiOiJodHRwczovL2FsYW5zY290dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNzM3YWNmYjM3ZDAwMDY4MjYwYTM3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNjg2MzA5OCwiZXhwIjoxNjE2OTQ5NDk4LCJhenAiOiJDdDRQSUI3MERBQ0kzUzdUSXpMc2JLUU15VDdnMTFiRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.ShRULsM67xJPU1Tggk491tVZV16G7QbdIIQUsJufxfi1DO4dAAT-b7gRAbEEj4j9XzlYhhbkMZn7wkhUF-jf4j0CKiIsKt8IpMb-hmnkvveNQ2Pcj-m19scpqLgRUAPu7UWz5Plw3dNdWGB42NcpZ9s1-tnLOsO9WqNK53vFA6KLlARxejcvqAwacX5-uyWpY_oQqmUHrpr0UosO4PbF6tq7JgqWONrLBG3xqi7pOsQP5JLDBYpR2Ou5zudGOaYiPS4AB2CCJbf9ATQ9Q7Vo75l_P3LKIBIi3MJ3CO5Px9InaB3B54S3KYGu9TAhFAebvrAjZjtTjSuekdUUvjKftQ"
CASTING_DIRECTOR_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRmTnY1WTltRjJNZEhZRjREWXNwLSJ9.eyJpc3MiOiJodHRwczovL2FsYW5zY290dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNzM3NDQ5ZDgxMWYwMDY5NmNhMTRmIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNjg2MzA0NSwiZXhwIjoxNjE2OTQ5NDQ1LCJhenAiOiJDdDRQSUI3MERBQ0kzUzdUSXpMc2JLUU15VDdnMTFiRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9yIiwiZGVsZXRlOmFjdG9yIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.FCN8Xd18Y4wLUABZmexQ7-IzKQE30tvIVKYog_7dh-4gYP3-mGgGnDRlmGS--8quTrjg2j1yci-bEtHX5u4UGKOhMhUhzZxLOudo3_m67u1XJxESMMwv-lbZ7kSiRKsL7BA14w6enaDc_MQGsI_bKfcdM3xAWqPFnUCjOHBjPFzRYAmgCS12_a6EMVGpfCofI9-1jGs-T269_aIQRUUE_Mj910NFEgdqt8niHSONNmzQk0WHDaCgxilmt1MjJn0dlvc2FZYYjFSfwFzSCUm_ESBKyBhSBx1TWzcHan8JuuIhnmJdH45c-h6ys8WRVrpDCRwRNxvJHcymIw_i1dL-dA"
EXECUTIVE_PRODUCER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRmTnY1WTltRjJNZEhZRjREWXNwLSJ9.eyJpc3MiOiJodHRwczovL2FsYW5zY290dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyYjYxMDZkYTNmYTIwMDZhYzlkYjQ2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNjg2Mjk0NywiZXhwIjoxNjE2OTQ5MzQ3LCJhenAiOiJDdDRQSUI3MERBQ0kzUzdUSXpMc2JLUU15VDdnMTFiRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9yIiwiY3JlYXRlOm1vdmllIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Ktw2KCfE0_2gndoHNafFEmcdHvdcYpt-1ZJ_ib95jGgd-SGN0rXAcxgK2cotqgQkcCSCsrTRtJco3mi_tp1xqjjZftnfR6_WffvgDDTKdUt6oOcXZr_wN5Ggp8fRWNwPyGEHjDvi6BSgReN8xKki7OZRL6wauT_Ydypntzh0ouk3xzae7AWK9Ur-C0QdVL7Pp8kkXWTKuPNXPdhtvfycu7pog36W8E5QUV-CydbVrqNAok5roOmAsBSKJqvTj0_Cmknv5hRw64G9C8TmJDkS-K7-l4-7Cpkg_8cgpVxNyvqnu-jlB5lNUVjgG76CFWsUW__smcrQeFRpiJBcwqAqqw"

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