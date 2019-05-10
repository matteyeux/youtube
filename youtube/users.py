import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash
import connexion

@app.route('/users')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT created_at, email, id, password, pseudo, username FROM user")
		rows = cursor.fetchall()
		if rows:
			result = {
				'message': 'OK',
				'data': rows
				# TODO : Add pager !!!
			}
			resp = jsonify(result)
			resp.status_code = 200
		else:
			result = {'message': 'not found'}
			resp = jsonify(result)
			resp.status_code = 404
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()