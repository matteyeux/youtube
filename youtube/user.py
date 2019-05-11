import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request, session
from werkzeug import generate_password_hash, check_password_hash
import connexion
import errors

@app.route('/user', methods=['POST'])
def add_user():
		_json = request.json
		_username = request.form.get('username')
		_email = request.form.get('email')
		_pseudo = request.form.get('pseudo')
		_password = request.form.get('password')
		if _username and _email and _pseudo and _password:
			_hashed_password = generate_password_hash(_password)
			sql = "INSERT INTO user(username, email, pseudo, password) VALUES(%s, %s, %s, %s)"
			data = (_username, _email, _pseudo, _hashed_password)
			try:
				conn = mysql.connect()
				cursor = conn.cursor(pymysql.cursors.DictCursor)
				cursor.execute(sql, data)
				cursor.execute("SELECT created_at, email, id, password, pseudo, username FROM user WHERE username=%s", _username)
				row = cursor.fetchone()
				conn.commit()
				cursor.close()
				result = {
					'message': 'OK',
					'data': row
				}
				resp = jsonify(result)
				resp.status_code = 200
				conn.close()
				return resp
			except Exception as e:
				print(e)
		else:
			return errors.not_found()

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

@app.route('/user', methods=['PUT'])
def update_user():
	try:
		_json = request.json
		_username = _json['username']
		_email = _json['email']
		_pseudo = _json['pseudo']
		_password = _json['pwd']
		# validate the received values
		if _name and _email and _password and _id and request.method == 'PUT':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "UPDATE user SET username=%s, email=%s, pseudo=%s, password=%s WHERE id=%s"
			data = (_name, _email, _hashed_password, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

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
		if row:
			return row
		else:
			return False
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

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
