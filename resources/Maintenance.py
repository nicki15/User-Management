from flask_restful import Resource


class Maintenance(Resource):

    def get(self):
        return {
            'message': "User-Management up and running.",
            'status': "all ok!"
        }
