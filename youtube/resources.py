from flask_restful import Resource, reqparse, request
from models import UserModel
from models import UserModel, TokenModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import datetime, uuid

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
			return {'message': 'User {} already exists'. format(data['username'])}, 400

		new_user = UserModel(
			username = data['username'],
			pseudo = data['pseudo'],
			email = data['email'],
			password = UserModel.generate_hash(data['password']),
			created_at = datetime.datetime.now()
		)
		try:
			new_user.save_to_db()
			access_token = create_access_token(identity = data['username'])
			refresh_token = create_refresh_token(identity = data['username'])

			current_user = UserModel.get_user_by_username(data['username'])
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
			return {'message': 'Something went wrong'}, 500

class UserAuthentication(Resource):
	def post(self):
		data = parser.parse_args()
		current_user = UserModel.get_user_by_username(data['username'])

		if not current_user:
			return {'message': 'User {} doesn\'t exist'.format(data['username'])}

		if UserModel.verify_hash(data['password'], current_user.password):
			#access_token = create_access_token(identity = data['username'])
			the_uuid = uuid.uuid4()
			insert_token_bdd(str(the_uuid), current_user.id)
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
			return {'message': 'Wrong credentials'}, 500

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


class SecretResource(Resource):
	#@jwt_required
	def get(self):
		if is_authentified():
			return {'answer': 'Message a la con'}
		else:
			return {'message': 'Vachier Cordialement'}


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
	else:
		return False

def actual_user_id():
	user = TokenModel.get_token_bdd(token=request.headers.get('Authorization'))
	if user:
		return user.user_id

def is_user_connected(id):
	user_id = actual_user_id()
	if user_id==id:
		print('BEWWWWAAA')
		return True
	else:
		print(user_id)
		return False