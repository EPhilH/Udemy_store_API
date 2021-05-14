from app import app
from db import db

db.init_app(app)

@app.before_first_request       #Using an inbuilt flask decorator.. the below function only runs before the very first request
def create_tables():            
    db.create_all()             #SQLAlchemy will create the tables in the database if they dont already exist. If they do exist it wont do anything.
