from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token

from database.database import User

#
# Sets up a parser of the http request that comes into the API
#
parser = reqparse.RequestParser()
parser.add_argument('username', help='username cannot be empty', required=True)
parser.add_argument('email', help='email cannot be empty', required=True)
parser.add_argument('password', help='password cannot be empty', required=True)


#
# setup a RESOURCE = an endpoint collection that could contain multiple access modi
#
class UserRegistration(Resource):

    def post(self):
        data = parser.parse_args()
        username = data['username']
        email = data['email']
        password = data['password']

        if User.find_by_username(username=username):
            return {'message': f'User {username} already exists!'}, 404

        new_user = User(name=username, email=email)
        new_user.set_password(password=password)

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                'message': f'User {username} was successfully created',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong!'}, 500
