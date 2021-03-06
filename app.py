import os

from flask import Flask
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func


from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL2', 'sqlite:///data.db') #Uses Heroku environment variable for SQlite... if runnig locally it wont find this so will then create a sqllite local database. 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This turns off Flasks modification tracker for SQLAlchemy, saves memory. SQLAlchemy has an inbuilt modification tracker.
app.secret_key = "Phil"
api = Api(app)



jwt = JWT(app, authenticate, identity) # JWT creates a new endpoint - /auth/

api.add_resource(Store,"/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug = True)

