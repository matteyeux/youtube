#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://youtube:youtube@localhost/youtube'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
	db.create_all()


app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
	jti = decrypted_token['jti']
	return models.RevokedTokenModel.is_jti_blacklisted(jti)


import views, models, resources, user

api.add_resource(resources.UserCreate, '/user')
api.add_resource(resources.UserAuthentication, '/auth')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(user.GetAllUsers, '/users')
api.add_resource(user.User, '/user/<int:id>')
api.add_resource(resources.SecretResource, '/secret')

if __name__ == '__main__' :
	app.run(debug=True, host='0.0.0.0', port=5000)
