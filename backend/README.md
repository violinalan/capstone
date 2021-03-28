# Casting Agency Backend

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server

From within the `./src` directory run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

## Authentication, Roles, and Permissions

The Casting Agency application has 3 roles:

1. Casting Assistant
    - Can view actors and movies
2. Casting Director
    - All permissions a Casting Assistant has
    - Add or delete an actor from the database
    - Modify actors or movies
3. Executive Producer
    - All permissions a Casting Director has
    - Add or delete a movie from the database

For this project, 3 users have been created in Auth0 to fulfill the 3 roles defined above:

1. Casting Assistant: 
    - Email: alanrscott@gmail.com
    - JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRmTnY1WTltRjJNZEhZRjREWXNwLSJ9.eyJpc3MiOiJodHRwczovL2FsYW5zY290dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNzM3YWNmYjM3ZDAwMDY4MjYwYTM3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNjg2MzA5OCwiZXhwIjoxNjE2OTQ5NDk4LCJhenAiOiJDdDRQSUI3MERBQ0kzUzdUSXpMc2JLUU15VDdnMTFiRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.ShRULsM67xJPU1Tggk491tVZV16G7QbdIIQUsJufxfi1DO4dAAT-b7gRAbEEj4j9XzlYhhbkMZn7wkhUF-jf4j0CKiIsKt8IpMb-hmnkvveNQ2Pcj-m19scpqLgRUAPu7UWz5Plw3dNdWGB42NcpZ9s1-tnLOsO9WqNK53vFA6KLlARxejcvqAwacX5-uyWpY_oQqmUHrpr0UosO4PbF6tq7JgqWONrLBG3xqi7pOsQP5JLDBYpR2Ou5zudGOaYiPS4AB2CCJbf9ATQ9Q7Vo75l_P3LKIBIi3MJ3CO5Px9InaB3B54S3KYGu9TAhFAebvrAjZjtTjSuekdUUvjKftQ

2. Casting Director:
    - Email: ashley@tierra.net
    - JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRmTnY1WTltRjJNZEhZRjREWXNwLSJ9.eyJpc3MiOiJodHRwczovL2FsYW5zY290dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNzM3NDQ5ZDgxMWYwMDY5NmNhMTRmIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNjg2MzA0NSwiZXhwIjoxNjE2OTQ5NDQ1LCJhenAiOiJDdDRQSUI3MERBQ0kzUzdUSXpMc2JLUU15VDdnMTFiRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9yIiwiZGVsZXRlOmFjdG9yIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.FCN8Xd18Y4wLUABZmexQ7-IzKQE30tvIVKYog_7dh-4gYP3-mGgGnDRlmGS--8quTrjg2j1yci-bEtHX5u4UGKOhMhUhzZxLOudo3_m67u1XJxESMMwv-lbZ7kSiRKsL7BA14w6enaDc_MQGsI_bKfcdM3xAWqPFnUCjOHBjPFzRYAmgCS12_a6EMVGpfCofI9-1jGs-T269_aIQRUUE_Mj910NFEgdqt8niHSONNmzQk0WHDaCgxilmt1MjJn0dlvc2FZYYjFSfwFzSCUm_ESBKyBhSBx1TWzcHan8JuuIhnmJdH45c-h6ys8WRVrpDCRwRNxvJHcymIw_i1dL-dA

3. Executive Producer:
    - Email: alan@tierra.net
    - JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRmTnY1WTltRjJNZEhZRjREWXNwLSJ9.eyJpc3MiOiJodHRwczovL2FsYW5zY290dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyYjYxMDZkYTNmYTIwMDZhYzlkYjQ2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNjg2Mjk0NywiZXhwIjoxNjE2OTQ5MzQ3LCJhenAiOiJDdDRQSUI3MERBQ0kzUzdUSXpMc2JLUU15VDdnMTFiRSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9yIiwiY3JlYXRlOm1vdmllIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Ktw2KCfE0_2gndoHNafFEmcdHvdcYpt-1ZJ_ib95jGgd-SGN0rXAcxgK2cotqgQkcCSCsrTRtJco3mi_tp1xqjjZftnfR6_WffvgDDTKdUt6oOcXZr_wN5Ggp8fRWNwPyGEHjDvi6BSgReN8xKki7OZRL6wauT_Ydypntzh0ouk3xzae7AWK9Ur-C0QdVL7Pp8kkXWTKuPNXPdhtvfycu7pog36W8E5QUV-CydbVrqNAok5roOmAsBSKJqvTj0_Cmknv5hRw64G9C8TmJDkS-K7-l4-7Cpkg_8cgpVxNyvqnu-jlB5lNUVjgG76CFWsUW__smcrQeFRpiJBcwqAqqw


## API Reference

### Getting Started
- Base URL: This backend API is hosted at https://alan-capstone.herokuapp.com/
- Authentication: The application is implemented with Auth0 authentication and JSON Web Tokens (JWT)

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 422: Not Processable

### Endpoints 

#### GET /movies
- General:
    - Returns an array of movie objects and success value
- Authorized Roles: 
    - Casting Assistant, Casting Director, Executive Producer
- Sample: `https://alan-capstone.herokuapp.com/movies`

```
{
    "movies": [
        {
            "id": 2,
            "title": "Ant-Man & Wasp",
            "year_released": 2015
        },
        {
            "id": 3,
            "title": "Doctor Strange",
            "year_released": 2017
        }
    ],
    "success": true
}
```

#### GET /actors
- General:
    - Returns an array of actor objects and success value
- Authorized Roles: 
    - Casting Assistant, Casting Director, Executive Producer
- Sample: `https://alan-capstone.herokuapp.com/actors`

```
{
    "actors": [
        {
            "age": 51,
            "gender": "Male",
            "id": 3,
            "name": "Paul Rudd"
        },
        {
            "age": 55,
            "gender": "Male",
            "id": 4,
            "name": "Robert Downey Jr."
        },
        {
            "age": 39,
            "gender": "Female",
            "id": 5,
            "name": "Scarlett Johansson"
        }
    ],
    "success": true
}
```

#### POST /movies
- General:
    - Returns an array with 1 movie object (including the newly created id), and success value
- Authorized Roles: 
    - Executive Producer
- Sample: `https://alan-capstone.herokuapp.com/movies`
    - Body: { "title": "The Incredible Hulk", "year_released": 2011 }

```
{
    "movies": [
        {
            "id": 4,
            "title": "The Incredible Hulk",
            "year_released": 2011
        }
    ],
    "success": true
}
```

#### POST /actors
- General:
    - Returns an array with 1 actor object (including the newly created id), and success value
- Authorized Roles: 
    - Casting Director, Executive Producer
- Sample: `https://alan-capstone.herokuapp.com/actors`
    - Body: { "name": "Elizabeth Olson", "age": 29, "gender": "Female" }

```
{
    "actors": [
        {
            "age": 29,
            "gender": "Female",
            "id": 6,
            "name": "Elizabeth Olson"
        }
    ],
    "success": true
}
```

#### PATCH /movies/{movie_id}
- General:
    - Returns an array with 1 movie object (including the updated fields), and success value
- Authorized Roles: 
    - Casting Director, Executive Producer
- Sample: `https://alan-capstone.herokuapp.com/movies/4`
    - Body: { "title": "The Incredible Hulkster" }

```
{
    "movies": [
        {
            "id": 4,
            "title": "The Incredible Hulkster",
            "year_released": 2011
        }
    ],
    "success": true
}
```

#### PATCH /actors/{actor_id}
- General:
    - Returns an array with 1 actor object (including the updated fields), and success value
- Authorized Roles: 
    - Casting Director, Executive Producer
- Sample: `https://alan-capstone.herokuapp.com/actors/6`
    - Body: { "name": "Elizabeth Olson (not the twin)" }

```
{
    "actors": [
        {
            "age": 29,
            "gender": "Female",
            "id": 6,
            "name": "Elizabeth Olson (not the twin)"
        }
    ],
    "success": true
}
```

#### DELETE /movies/{movie_id}
- General:
    - Returns the deleted id and success value
- Authorized Roles: 
    - Executive Producer
- Sample: `https://alan-capstone.herokuapp.com/movies/4`

```
{
    "delete": 4,
    "success": true
}
```

#### DELETE /actors/{actor_id}
- General:
    - Returns the deleted id and success value
- Authorized Roles: 
    - Casting Director, Executive Producer
- Sample: `https://alan-capstone.herokuapp.com/actors/6`

```
{
    "delete": 6,
    "success": true
}
```


## Deployment
The application is deployed on Heroku. The following environment variables are set in the Heroku dashboard:
- DATABASE_URL: postgres://uwmmdlhsbkftvo:4e3fa44f2aafcf456eef985f7a42cfabec134e192ae6878a4d1d5b5f86a0ae28@ec2-54-225-190-241.compute-1.amazonaws.com:5432/d7fata0a04nr6m
- AUTH0_DOMAIN: alanscott.us.auth0.com
- ALGORITHMS: ['RS256']
- API_AUDIENCE: casting

## Authors
Alan Scott

## Acknowledgements 
Thank you all.

## Unit Testing
To run the unit tests, run
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < src/database/capstone.psql
python test_capstone.py
```