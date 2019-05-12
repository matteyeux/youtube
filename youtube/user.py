from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import app
import jwt

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

	def encode_auth_token(self, user_id):
		"""
		Generates the Auth Token
		:return: string
		"""
		try:
			payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
				'iat': datetime.datetime.utcnow(),
				'sub': user_id
			}
			return jwt.encode(
				payload,
				app.config.get('SECRET_KEY'),
				algorithm='HS256'
			)
		except Exception as error:
			return error	

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