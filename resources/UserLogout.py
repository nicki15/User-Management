from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from database.models import User, RevokedToken


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_identity = get_jwt_identity()   # = json webtoken identity (jti) = (unique) username
        token = get_jwt()['jti']            # token = dict -> ['jti'] is the actual token identity

        try:
            user = User.find_by_username(username=jwt_identity)
            if user:
                revoked_token = RevokedToken(_token=token, _issuer_id=user.id)
                revoked_token.save_to_db()
                return {'message': 'Access token successfully revoked'}
            else:
                return {'message': 'User does not exist'}, 500
        except:
            return {'message': 'Something went wrong'}, 500
