import sys
sys.path.insert(0, r'../../mailer')
import mailer

from flask_restful import Resource, reqparse
from models import UserModel, TokenModel
from resources import is_authentified, actual_user_id, is_user_connected, paging, number_page
import re

class User(Resource):
	# Get user information
	def get(self, id):
		result = UserModel.get_user_by_id(id)
		if result:
			data = {
				'id': result.id,
				'username': result.username,
				'pseudo': result.pseudo,
				'created_at': str(result.created_at),
			}
			if is_user_connected(id):
				data.update({'email': result.email})
			return {'message': 'OK', 'data': data}
		else:
			return {'message': 'Not found'}, 404

	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('username', help='This field cannot be blank', required=True)
		parser.add_argument('pseudo', help='This field cannot be blank', required=False)
		parser.add_argument('email', help='This field cannot be blank', required=False)
		parser.add_argument('password', help='This field cannot be blank', required=True)
		data = parser.parse_args()

		data_user = UserModel(
			id=id,
			username=data['username'],
			pseudo=data['pseudo'],
			email=data['email'],
			password=UserModel.generate_hash(data['password'])
		)

		if is_authentified()!=True:
			return {'message': 'Unauthorized'}, 401
		if is_user_connected(id)!=True:
			return {'message': 'Forbidden'}, 403

		result = UserModel.get_user_by_id(id)
		if result:
			#check email
			if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data.email) is None:
				return {
					'message': 'Bad Request', 
					'Code': '1002 => invalid email format',
					'data': {
						'username': data['username'],
						'pseudo': data['pseudo'],
						'email': data['email']
						}
					}, 400

			check_by_username = UserModel.get_user_by_username(data_user.username)
			if check_by_username and check_by_username.id!=id:
				return {
					'message': 'Bad Request',
					'code': '1001 => User {} already exists'. format(data['username']),
					'data': {
						'username': data['username'],
						'pseudo': data['pseudo'],
						'email': data['email']
						}
					}, 400

			check_by_email = UserModel.get_user_by_email(data_user.email)
			if check_by_email and check_by_email.id!=id:
				return {
					'message': 'Bad Request',
					'code': '1002 => email {} already exists'. format(data['email']),
					'data': {
						'username': data['username'],
						'pseudo': data['pseudo'],
						'email': data['email']
						}
					}, 400

			UserModel.update_user_by_id(data_user)
			result = UserModel.get_user_by_id(id)
			data = {
				'id': result.id,
				'username': result.username,
				'pseudo': result.pseudo,
				'created_at': str(result.created_at),
				'email': result.email
			}
			
			mailer.send_mail(1, data['email'])
			return {'message': 'OK', 'data': data}
		else:
			return {'message': 'Not found'}, 404

	# Delete user
	def delete(self, id):
		if is_authentified()!=True:
			return {'message': 'Unauthorized'}, 401
		result = UserModel.get_user_by_id(id)
		if result and is_user_connected(id):
			TokenModel.delete_all_token_by_user_id(id)
			UserModel.delete_user_by_id(id)
			return {}, 204
		elif result:
			return {'message': 'Forbidden'}, 403
		else:
			return {'message': 'Not found'}, 404


# List all users
class GetAllUsers(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('pseudo', help='This field cannot be blank', required=False)
		parser.add_argument('page', help='This field cannot be blank', required=False)
		parser.add_argument('perPage', help='This field cannot be blank', required=False)
		json = parser.parse_args()

		result = UserModel.get_all_users(json['pseudo'])
		page = json['page']
		perPage = json['perPage']
		datum = []

		for data in result:
			if is_user_connected(data.id):
				datum.append({
					'id': data.id,
					'username': data.username,
					'pseudo': data.pseudo,
					'created_at': str(data.created_at),
					'email': data.email
				})
			else:
				datum.append({
						'id': data.id,
						'username': data.username,
						'pseudo': data.pseudo,
						'created_at': str(data.created_at)
					})

		if page is None:
			page = 1
		if perPage is None:
			perPage = 100
		results = paging(datum, int(page), int(perPage))
		total_page = number_page(datum, int(perPage))

		if results:
			return { 
				'message': 'OK', 
				'data': results,
				'pager': {
					'current': page,
					'total': total_page
					}
				}, 200
		else:
			return {'message': 'Not found'}, 404
