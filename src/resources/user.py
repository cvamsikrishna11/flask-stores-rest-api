from flask_restful import Resource, reqparse
from src.models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field can"t be left blank')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field can"t be left blank')

    def post(self):
        user_data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(username=user_data['username']):
            return {'message': 'A user with username already exists'}, 400
        user = UserModel(user_data['username'], user_data['password'])
        user.save_to_db()
        return {"message": "user created successfully"}, 201
