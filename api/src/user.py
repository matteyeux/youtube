from flask_restful import Resource, reqparse
from models import UserModel, TokenModel
from resources import is_authentified, actual_user_id, is_user_connected
import jsonify

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
			return { 'message': 'OK', 'data': data}
		else:
			return { 'message': 'Not found'}, 404

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
			return {"message": "Unauthorized"}, 401
		if is_user_connected(id)!=True:
			return {"message": "Forbidden"}, 403

		result = UserModel.get_user_by_id(id)
		if result:
			check_by_username = UserModel.get_user_by_username(data_user.username)
			if check_by_username and check_by_username.id!=id:
				return {"message": "Bad Request", 'Code': "1001 => username existe déja"}

			check_by_email = UserModel.get_user_by_email(data_user.email)
			if check_by_email and check_by_email.id!=id:
				return {"message": "Bad Request", 'Code': "1002 => email existe déja"}

			UserModel.update_user_by_id(data_user)
			result = UserModel.get_user_by_id(id)
			data = {
				'id': result.id,
				'username': result.username,
				'pseudo': result.pseudo,
				'created_at': str(result.created_at),
				'email': result.email
			}
			return {'message': 'OK', 'data': data}
		else:
			return {'message': 'Not found'}, 404

	# Delete user
	def delete(self, id):
		if is_authentified()!=True:
			return {"message": "Unauthorized"}, 401
		result = UserModel.get_user_by_id(id)
		if result and is_user_connected(id):
			TokenModel.delete_all_token_by_user_id(id)
			UserModel.delete_user_by_id(id)
			return {}, 204
		elif result:
			return {"message": "Forbidden"}, 403
		else:
			return { 'message': 'Not found'}, 404


# List all users
class GetAllUsers(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('pseudo', help='This field cannot be blank', required=False)
		json = parser.parse_args()

		result = UserModel.get_all_users(json["pseudo"])
		datum = []
		for data in result:
			datum.append({
				'id': data.id,
				'username': data.username,
				'pseudo': data.pseudo,
				'created_at': str(data.created_at),
				'email': data.email
			})
		#user_list = UserModel.get_all_users()
		if result:
			return { 'message': 'OK', 'data': datum }
		else:
			return { 'message': 'Not found'}, 404

	#def delete(self):
	#	return UserModel.delete_all()





"""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import app

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(45), unique=True)
	email = db.Column(db.String(45), unique=True)
	pseudo = db.Column(db.String(45), unique=True)
	password = db.Column(db.String(128), unique=True)

	def __init__(self, username, email, pseudo, password):
		self.username = username
		self.email = email
		self.pseudo = pseudo
		self.password = password

class UserSchema(ma.Schema):
	class Meta:
		fields = ('username', 'email', 'pseudo', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
	username = request.json['username']
	email = request.json['email']
	pseudo = request.json['pseudo']
	password = request.json['password']

	new_user = User(username, email, pseudo, password)
	result = user_schema.dump(new_user)

	db.session.add(new_user)
	db.session.commit()

	resp = user_schema.jsonify(new_user)
	resp.status_code = 201
	return resp

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import app

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(45), unique=True)
	email = db.Column(db.String(45), unique=True)
	pseudo = db.Column(db.String(45), unique=True)
	password = db.Column(db.String(128), unique=True)

	def __init__(self, username, email, pseudo, password):
		self.username = username
		self.email = email
		self.pseudo = pseudo
		self.password = password

class UserSchema(ma.Schema):
	class Meta:
		fields = ('username', 'email', 'pseudo', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
	username = request.json['username']
	email = request.json['email']
	pseudo = request.json['pseudo']
	password = request.json['password']

	new_user = User(username, email, pseudo, password)
	result = user_schema.dump(new_user)

	db.session.add(new_user)
	db.session.commit()

	resp = user_schema.jsonify(new_user)
	resp.status_code = 201
	return resp




# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])
def user_details(id):
	user = User.query.get(id)
	return user_schema.jsonify(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
	user = User.query.get(id)
	username = request.json['username']
	email = request.json['email']

	user.email = email
	user.username = username

	db.session.commit()
	return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
	user = User.query.get(id)
	db.session.delete(user)
	db.session.commit()

	return user_schema.jsonify(user)


# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])
def user_details(id):
	user = User.query.get(id)
	return user_schema.jsonify(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
	user = User.query.get(id)
	username = request.json['username']
	email = request.json['email']

	user.email = email
	user.username = username

	db.session.commit()
	return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
	user = User.query.get(id)
	db.session.delete(user)
	db.session.commit()

	return user_schema.jsonify(user)
"""