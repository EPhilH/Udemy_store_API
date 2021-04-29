import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel





class UserRegister(Resource):  # We use resource so that the class can be used as a Flask API Endpoint.

    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type=str,
        required = True,
        help="This field cannot be left blank!"
        )
    parser.add_argument("password",
        type=str,
        required = True,
        help="This field cannot be left blank!"
        )


    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):  # basically means if User is not NONE, then do this (ie user exists)
            return {"message" : "User already exists"}, 400
        
        user=UserModel(data["username"], data["password"])
        user.save_to_db()
        

        return {"message" : "User created successfully."} , 201

