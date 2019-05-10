import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash
import connexion

@app.errorhandler(400)
def bad_request(error=None):
	message = {
		'message': 'Bad Request',
		'code' : 'xxx' # <- not sure what to do with it
		#'data' : [] commented for the moment
	}

	resp = jsonify(message)
	resp.status_code = 400
	return resp


@app.errorhandler(401)
def unauthorized(error=None):
	message = {
		'message': 'Unauthorized'
	}

	resp = jsonify(message)
	resp.status_code = 401
	return resp

@app.errorhandler(403)
def forbidden(error=None):
	message = {
		'message': 'Forbidden'
	}

	resp = jsonify(message)
	resp.status_code = 403

	return resp

@app.errorhandler(404)
def not_found(error=None):
	message = {
		#'status': 404,
		'message': 'Not found'
	}

	resp = jsonify(message)
	resp.status_code = 404
	return resp

@app.errorhandler(405)
def not_allowed(error=None):
	message = {
		#'status': 404,
		'message': 'Not allowed'
	}

	resp = jsonify(message)
	resp.status_code = 405
	return resp