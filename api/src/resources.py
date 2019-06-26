import sys
sys.path.insert(0, r'../../mailer')
import mailer

from flask_restful import Resource, reqparse, request
from models import UserModel
from models import UserModel, TokenModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import datetime, uuid, re

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('pseudo', help = 'This field cannot be blank', required = False)
parser.add_argument('email', help = 'This field cannot be blank', required = False)
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('created_at', help = 'This field cannot be blank', required = False)


class UserCreate(Resource):
	def post(self):
		data = parser.parse_args()

		if UserModel.get_user_by_username(data['username']):
			return {
				'message': 'Bad Request',
				'code': '1001 => User {} already exists'. format(data['username']),
				'data': {
					'username': data['username'],
					'pseudo': data['pseudo'],
					'email': data['email']
					}
				}, 400

		if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data['email']) is None:
			return {
				'message': 'Bad Request', 
				'Code': '1002 => format email invalide',
				'data': {
					'username': data['username'],
					'pseudo': data['pseudo'],
					'email': data['email']
					}
				}, 400

		check_by_email = UserModel.get_user_by_email(data['email'])
		if check_by_email:
			return {
				'message': 'Bad Request',
				'code': '1002 => email {} already exists'. format(data['email']),
				'data': {
					'username': data['username'],
					'pseudo': data['pseudo'],
					'email': data['email']
					}
				}, 400

		new_user = UserModel(
			username = data['username'],
			pseudo = data['pseudo'],
			email = data['email'],
			password = UserModel.generate_hash(data['password']),
			created_at = datetime.datetime.now()
		)
		try:
			new_user.save_to_db()
			current_user = UserModel.get_user_by_username(data['username'])
			access_token = create_access_token(identity = data['username'])
			refresh_token = create_refresh_token(identity = data['username'])
			mailer.send_mail(0, current_user.email)
			return {
				'message': 'OK',
				'data': {
					'id': current_user.id,
					'username': current_user.username,
					'pseudo': current_user.pseudo,
					'created_at': str(current_user.created_at),
					'email': current_user.email
					}
			}, 201
		except:
				return {'message': 'Fatal Error'}, 500

class UserAuthentication(Resource):
	def post(self):
		data = parser.parse_args()
		current_user = UserModel.get_user_by_username(data['username'])

		if not current_user:
			return {
				'message': 'Bad Request',
				'code': '1003 => User {} doesn\'t exist'.format(data['username']),
				'data': {
					'username': data.username
					}
				}, 400

		if UserModel.verify_hash(data['password'], current_user.password):
			the_uuid = uuid.uuid4()
			insert_token_bdd(str(the_uuid), current_user.id)
			access_token = create_access_token(identity = data['username'])
			refresh_token = create_refresh_token(identity = data['username'])
			return {
				'message': 'OK',
				'data': {
					'token': str(the_uuid),
					'user': {
						'id': current_user.id,
						'username': current_user.username,
						'pseudo': current_user.pseudo,
						'created_at': str(current_user.created_at),
						'email': current_user.email
						}
					}
				}, 201
		else:
			return {
				'message': 'Bad Request',
				'code': '1004 => Wrong credentials',
				'data': {
					'username': data.username
					}
				}, 400

class UserLogoutAccess(Resource):
	@jwt_required
	def post(self):
		jti = get_raw_jwt()['jti']
		try:
			revoked_token = RevokedTokenModel(jti = jti)
			revoked_token.add()
			return {'message': 'Access token has been revoked'}
		except:
			return {'message': 'Something went wrong'}, 500

class UserLogoutRefresh(Resource):
	@jwt_refresh_token_required
	def post(self):
		jti = get_raw_jwt()['jti']
		try:
			revoked_token = RevokedTokenModel(jti = jti)
			revoked_token.add()
			return {'message': 'Refresh token has been revoked'}
		except:
			return {'message': 'Something went wrong'}, 500

class TokenRefresh(Resource):
	@jwt_refresh_token_required
	def post(self):
		current_user = get_jwt_identity()
		access_token = create_access_token(identity = current_user)
		return {'access_token': access_token}


def insert_token_bdd(token, user_id):
	insert_token = TokenModel(
		code=token,
		user_id=user_id,
		expired_at=datetime.datetime.now()
	)
	try:
		insert_token.save_to_db()
	except:
		return {}, 500

def is_authentified():
	if TokenModel.get_token_bdd(token=request.headers.get('Authorization')):
		return True

def actual_user_id():
	user = TokenModel.get_token_bdd(token=request.headers.get('Authorization'))
	if user:
		return user.user_id

def is_user_connected(id):
	user_id = actual_user_id()
	if user_id==id:
		return True
	else:
		return False

def paging(results, page=1, perPage=100):
	first_id_result = (page - 1) * perPage
	last_id_result = (page * perPage)

	if last_id_result > len(results):
		last_id_result = len(results)

	new_results = []
	i = first_id_result
	while i < last_id_result:
		new_results.append(results[i])
		if i < last_id_result:
			i = i + 1

	return new_results

def number_page(results, perPage=100):
	total_page = int(len(results) / perPage) + (len(results) % perPage > 0)
	return total_page
