import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request, session
from werkzeug import generate_password_hash, check_password_hash
import connexion
import errors

# GET USER
@app.route('/user/<int:id>', methods=['GET'])
def user(id):
	row = get_user_sql_from_id(id)
	if row:
		result = {
			'message': 'OK',
			'data': row
		}
		resp = jsonify(result)
		resp.status_code = 200
	else:
		return errors.not_found()
	return resp


# CREATE USER
@app.route('/user', methods=['POST'])
def add_user():
		_json = request.json
		_username = request.form.get('username')
		_email = request.form.get('email')
		_pseudo = request.form.get('pseudo')
		_password = request.form.get('password')
		if _username and _email and _pseudo and _password:
			row = insert_user_sql(_username, _email, _pseudo, _password)
			result = {
				'message': 'OK',
				'data': row
			}
			resp = jsonify(result)
			resp.status_code = 200
			return resp
		else:
			return errors.not_found()


# UPDATE USER
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
	row = get_user_sql_from_id(id)
	if row:
		_json = request.json
		_username = request.form.get('username')
		_email = request.form.get('email')
		_pseudo = request.form.get('pseudo')
		_password = request.form.get('password')
		if _username and _email and _pseudo and _password:
			row = update_user_sql(id, _username, _email, _pseudo, _password)
			result = {
				'message': 'OK',
				'data': row
			}
			resp = jsonify(result)
			resp.status_code = 200
			return resp
		else:
			return errors.not_found()
	else:
		return errors.not_found()


# DELETE USER
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
	row = get_user_sql_from_id(id)
	if row:
		delete_user_sql(id)
		resp = jsonify('User deleted successfully!')
		resp.status_code = 204
	else:
		return errors.not_found()
	return resp



# TODO : Delete it later or change to the swagger url (if possible)
@app.route('/')
def home():
	message = {
		'status': 200,
		'message': 'home'
	}

	resp = jsonify(message)
	resp.status_code = 200

	return resp



def get_user_sql_from_id(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT created_at, email, id, password, pseudo, username FROM user WHERE id=%s", id)
		row = cursor.fetchone()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	if row:
		return row
	else:
		return False


def get_user_sql_from_pseudo(pseudo):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT created_at, email, id, password, pseudo, username FROM user WHERE pseudo=%s", pseudo)
		row = cursor.fetchone()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	if row:
		return row
	else:
		return False


def delete_user_sql(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM user WHERE id=%s", id)
		conn.commit()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()


def insert_user_sql(username, email, pseudo, password):
	hashed_password = generate_password_hash(password)
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "INSERT INTO user(username, email, pseudo, password) VALUES(%s, %s, %s, %s)"
		data = (username, email, pseudo, hashed_password)
		cursor.execute(sql, data)
		conn.commit()
		row = get_user_sql_from_pseudo(pseudo)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	if row:
		return row
	else:
		return False


def update_user_sql(id, username, email, pseudo, password):
	hashed_password = generate_password_hash(password)
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		#sql = "INSERT INTO user(username, email, pseudo, password) VALUES(%s, %s, %s, %s)"
		sql = "UPDATE user SET username = %s, email = %s, pseudo = %s, password = %s WHERE id=%s"
		data = (username, email, pseudo, hashed_password, id)
		cursor.execute(sql, data)
		conn.commit()
		row = get_user_sql_from_id(id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	if row:
		return row
	else:
		return False