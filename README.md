# **Introduction**
This application serves as a content management system for a film production company, providing the ability to manage actors and movies. Through the provided endpoints, users can create, read, update, and delete movie and actor records in the database.

# **Motivation Behind The Project**
The primary purpose of building this application is to provide a robust back-end system that manages and keeps track of actors and movies. As film production companies often work with various actors and produce multiple movies, having a reliable system to manage this data becomes crucial.

# **Tech Stack Used In The Project**
**Flask**: A lightweight WSGI web application framework.
**SQLAlchemy**: The Python SQL toolkit and Object-Relational Mapping (ORM) library.
**PostgreSQL**: The open-source relational database.
**Flask-CORS**: A Flask extension for handling Cross-Origin Resource Sharing (CORS).
**Render**: Cloud platform for deploying, managing, and scaling apps.

# **Installation Instructions**
pip3 install -r requirements.txt

# **Set up the database URL in your environment**
```
export DATABASE_URL="postgresql://postgres:120598@localhost:5432/capstone"
export EXCITED="true"
```

# **Run on local**
```
python manage.py runserver
```

# **Testing Instructions**
1. Ensure you have the testing database set up and updated the DATABASE_URL if necessary.
2. Run the tests using the following command:
          python -m unittest test_app.py
Roles and the Permissions Associated With It
* **Casting Assistant**:
  * get:actors
  * get:movies
* **Casting Director** (Has all the permissions of Casting Assistant plus):
  * post:actors
  * delete:actors
  * patch:actors
  * patch:movies
* **Executive Producer** (Has all the permissions of Casting Director plus):
  * post:movies
  * delete:movies
 
# **Documentation of the APIs**
Token auth0 to using Postman:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRNUTFJWVZiVFhYSFRjaU9iWGMtQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1sOGxmc3MxZGU4eHltaWZ5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJqU3lJUmFKb2Ridm9XWW5DOXpZbmFvaGxqQjBhVE9JcUBjbGllbnRzIiwiYXVkIjoiQ2Fwc3RvbmVfdWRhY2l0eSIsImlhdCI6MTY5NjA2MjE1MiwiZXhwIjoxNjk2MTQ4NTUyLCJhenAiOiJqU3lJUmFKb2Ridm9XWW5DOXpZbmFvaGxqQjBhVE9JcSIsInNjb3BlIjoiZ2V0OmFjdG9ycyBnZXQ6bW92aWVzIHBvc3Q6YWN0b3JzIGRlbGV0ZTphY3RvcnMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBkZWxldGU6bW92aWVzIHBvc3Q6bW92aWVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJkZWxldGU6bW92aWVzIiwicG9zdDptb3ZpZXMiXX0.easSkGGr_gGZAq8_WCu3ZPtrohfSlPWSTwpCGQGY76K2PKjA_987YmkJ_UIpLL0y1eAKL9QQd1yR-Qtk5NXrOaoh6DRfM4rbRx1qSCOOGVIgDe9PRJVP7eCULo-vTUORcYWOcfKb_RwbaQ-3_wmLeCTYAa4TDsKaXCUboUP6q_U-KvOMyJtysU7akuwFRTcifZq0VSde-Zl33gNdGVh7V2SNKK9TV5WMyuooa4z4kRmiTyAIA2JGJ-MM2x2JgExWcKD2NyIFYLClmlIjX-fqI8_8TSebLsJFowb9IMHfOt7ucia_1Xx5LsJMhLJP5t4hjBLwXcfZbfFm_ssvismaLg

Type: Bearer

**get:/actors**
output
```json
{
    "actors": [
        {
            "age": 30,
            "gender": "male",
            "id": 1,
            "name": "Tu"
        },
}
```
**get:movies**
```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 11 Dec 1998 17:00:00 GMT",
            "title": "Enjoy my life"
        },
}
```
**post:actors**
in postman, body (raw -> json)
```json
{
  "name": "Tu",
  "age": 30,
  "gender": "male"
}
```

**post:movies**
in postman, body (raw -> json)
```json
{
    "title": "Enjoy life",
    "release_date": "2022-09-09"
}
```


# **Render Link**
The backend application has been deployed on Heroku and can be accessed live at:
```
https://capstone-cncy.onrender.com/
```


