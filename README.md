# Capstone Project - Casting Agency

## About
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
The backend system are capable to get list of all actors, add a new actor, edit an existing actor record, delete an existing actor record as well as to get list of all movies, add a new movie, edit an existing movie record, delete an existing movie record though their apropriate endpoint.
The project also utilizes Auth0 for role-based access control.

The endpoints and how to send requests to these endpoints for products and items are described in the 'Endpoint Library' section of the README.

All endpoints need to be tested using the test_app.py script since there is no frontend for the app yet.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

In the warranty-tracker directory, run the following to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

To run the server, execute:
```
python3 app.py
```
We can now also open the application via Heroku using the URL:
https://capstone2121.herokuapp.com

The endpoints have to be tested using test_app.py script
using the token since I did not build a frontend for the application.

## DATA MODELING:
#### models.py
The schema for the database and helper methods to simplify API behavior are in models.py:
- There are two tables created: Actor and Movie
- The Actor table has id (primary key), age, and gender.
- The Movie table has id (primary key), and date.
Each table has an insert, update, delete, and format helper functions.

## ROLE BASED ACCESS CONTROL:
#### Casting Assistant
Permission include: get:actors, get:movies
#### Casting Director
Permission include: get:actors, get:movies, post:actors, patch:actors, patch:movies, delete:actors
#### Executive Director
Permission include: get:actors, get:movies, post:actors, post:movies, patch:actors, patch:movies, delete:actors, delete:movies

## API ARCHITECTURE AND TESTING
### Endpoint Library

@app.errorhandler decorators were used to format error responses as JSON objects. Custom @requires_auth decorator were used for Authorization based
on roles of the user. Three roles are assigned to this API: 'Casting Assistant', 'Casting Director' and 'Executive Director'.
All the role is need to be pre-assigned to certain users.

A token needs to be passed to each endpoint. 
The token can be retrived by following these steps:
1. Go to: https://fsnd21.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=L5gNkzVzN9bJlTLDLuWt9MQChBDCo7Ck&redirect_uri=https://127.0.0.1:8080/login-result
2. Login to one of this account with their pre-assigned role:
    Casting Assistant
    Email   : swqeasitbssfuxlrmy@miucce.com
    Pass    : !1Qwerty

    Casting Director
    Email   : enlcssumsuvjzqpokz@kiabws.com
    Pass    : !1Qwerty

    Executive Producer
    Email   : kxsmgkotguzncspvpb@wqcefp.com
    Pass    : !1Qwerty


#### GET '/movies'
Returns a list of all available movies and a success value
Sample response output:
{
  "movies": [
    {
      "title": "test",
      "id": 1,
      "date": "2021-11-11",
    }
  ],
  "success": true
}

#### POST '/movies'
Returns the newly added movie record and a success value
Sample response output:
{
  "movie": {
      "title": "test",
      "id": 1,
      "date": "2021-11-11",
    },
  "success": true
}

#### PATCH '/movies/{movie_id}'
Returns the newly patched movie record and a success value
Sample response output:
{
  "movie": {
      "title": "test1",
      "id": 1,
      "date": "2021-11-11",
    },
  "success": true
}

#### DELETE '/movies/{movie_id}'
Returns deleted 1 and a success value
Sample response output:
{
  "deleted": 1,
  "success": true
}

#### GET '/actors'
Returns a list of all available actors and a success value
Sample response output:
{
  "actors": [
    {
      "name": "test",
      "id": 1,
      "age": 1,
      "gender": "male",
    }
  ],
  "success": true
}

#### POST '/actors'
Returns the newly added actor record and a success value
Sample response output:
{
  "actor": {
      "name": "test",
      "id": 1,
      "age": 1,
      "gender": "male",
    },
  "success": true
}

#### PATCH '/actors/{actor_id}'
Returns the newly patched actor record and a success value
Sample response output:
{
  "actor": {
      "name": "test1",
      "id": 1,
      "age": 1,
      "gender": "male",
    },
  "success": true
}

#### DELETE '/actors/{movactor_idie_id}'
Returns deleted 1 and a success value
Sample response output:
{
  "deleted": 1,
  "success": true
}

## Testing
There are 20 unittests in test_app.py. To run this file first change the refresh the token inside it through credentals provided above,
And use:
```
python test_app.py
```
The tests include one test for expected success and error behavior for each endpoint, and tests demonstrating role-based access control,
with each role given two test (one success and one error behavior except executive director which has full access).

## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the 'Casting Assistant', 'Casting Director' and 'Executive Directore' roles.

## DEPLOYMENT
The app is hosted live on heroku at the URL: 
https://capstone2121.herokuapp.com

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with the test_app.py.