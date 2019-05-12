from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        new_user = UserModel(
            username = data['username'],
            email = data['email'],
            pseudo = data['pseudo'],
            password = data['password']
        )
        try:
            new_user.save_to_db()
            return {
                'message': 'User {} was created'.format( data['username'])
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        return data

      
class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}
      
      
class AllUsers(Resource):
    def get(self):
        return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}
      
      
class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }