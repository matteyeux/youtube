from flask_restful import Resource, reqparse
from models import UserModel
from resources import is_authentified, actual_user_id
import jsonify


class User(Resource):
	# Get user information
	def get(self, id):
		result = UserModel.get_user_by_id(id)
		user_id = actual_user_id()
		data = {
			'id': result.id,
			'username': result.username,
			'pseudo': result.pseudo,
			'created_at': str(result.created_at),
		}
		if user_id==id:
			data.update({'email': result.email})
		if result:
			return { 'message': 'OK', 'data': data}
		else:
			return { 'message': 'Not found'}, 404

	# Delete user
	def delete(self, id):
		result = UserModel.get_user_by_id(id)
		if result:
			UserModel.delete_user_by_id(id)
			return {}, 204
		else:
			return { 'message': 'Not found'}, 404


# List all users
class GetAllUsers(Resource):
	def get(self):
		return UserModel.get_all_users()

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