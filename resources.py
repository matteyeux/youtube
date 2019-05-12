from flask_restful import Resource, reqparse
from models import UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('email', help = 'This field cannot be blank', required = False)
parser.add_argument('pseudo', help = 'This field cannot be blank', required = False)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


class UserRegistration(Resource):
	def post(self):
		data = parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {'message': 'User {} already exists'. format(data['username'])}

		new_user = UserModel(
			username = data['username'],
			email = data['email'],
			pseudo = data['pseudo'],
			password = UserModel.generate_hash(data['password'])
		)
		try:
			new_user.save_to_db()
			access_token = create_access_token(identity = data['username'])
			refresh_token = create_refresh_token(identity = data['username'])
			return {
				'message': 'User {} was created'.format( data['username']),
				'access_token': access_token,
				'refresh_token': refresh_token
			}
		except:
			return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
	def post(self):
		data = parser.parse_args()
		current_user = UserModel.find_by_username(data['username'])

		if not current_user:
			return {'message': 'User {} doesn\'t exist'.format(data['username'])}
		
		if UserModel.verify_hash(data['password'], current_user.password):
			access_token = create_access_token(identity = data['username'])
			refresh_token = create_refresh_token(identity = data['username'])
			return {
				'message': 'Logged in as {}'.format(current_user.username),
				'access_token': access_token,
				'refresh_token': refresh_token
				}
		else:
			return {'message': 'Wrong credentials'}

	  
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
		return UserModel.return_all()
	
	def delete(self):
		return UserModel.delete_all()
	  
	  
class SecretResource(Resource):
	def get(self):
		return {
			'answer': 42
		}