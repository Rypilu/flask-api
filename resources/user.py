import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"Message": f"Username {data.get('username')} already exists, please try again"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return{"message": f"User {data.get('username')} created successfully."}, 201


