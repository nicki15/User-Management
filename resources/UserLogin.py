from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token

from database.models import User

parser = reqparse.RequestParser()
parser.add_argument('username', help='username cannot be empty', required=True)
parser.add_argument('password', help='password cannot be empty', required=True)


class UserLogin(Resource):

    def post(self):
        data = parser.parse_args()
        username = data['username']
        password = data['password']

        current_user = User.find_by_username(username=username)
        if not current_user:
            return {'message': f'User {username} does not exist!'}

        if User.check_password(password=password, _hash=current_user.password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                'message': f'Logged in as User: {username}',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Invalid credentials'}
