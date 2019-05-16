from youtube import db
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

class TokenModel(db.Model):
	__tablename__ = 'token'

	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(120), unique=True, nullable=False)
	user_id = db.Column(db.Integer, nullable=False)
	expired_at = db.Column(db.Date, nullable=False)

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def get_token_bdd(cls, token):
		return cls.query.filter_by(code = token).first()

	@classmethod
	def delete_all_token_by_user_id(cls, user_id):
		return cls.query.filter_by(user_id = user_id).delete()


class UserModel(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(120), unique = True, nullable = False)
	email = db.Column(db.String(120), unique = True, nullable = False)
	pseudo = db.Column(db.String(120), nullable = False)
	password = db.Column(db.String(120), nullable = False)
	created_at = db.Column(db.Date, nullable = False)

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def update_user_by_id(cls, data):
		user = cls.query.filter_by(id=data.id).first()
		user.pseudo = data.pseudo
		user.email = data.email
		user.password = data.password
		db.session.commit()

	@classmethod
	def get_user_by_username(cls, username):
		return cls.query.filter_by(username = username).first()

	@classmethod
	def get_user_by_id(cls, id):
		return cls.query.filter_by(id = id).first()

	@classmethod
	def delete_user_by_id(cls, id):
		result = cls.query.filter_by(id = id).delete()
		db.session.commit()
		return result

	@classmethod
	def get_all_users(cls):
		def to_json(x):
			return {
				'id': x.id,
				'username': x.username,
				'pseudo': x.pseudo,
				'created_at': str(x.created_at)
			}
		return {
			'message': 'OK',
			'data': list(map(lambda x: to_json(x), UserModel.query.all()))
		}

	"""
	@classmethod
	def delete_all(cls):
		try:
			num_rows_deleted = db.session.query(cls).delete()
			db.session.commit()
			return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
		except:
			return {'message': 'Something went wrong'}
	"""

	@staticmethod
	def generate_hash(password):
		return sha256.hash(password)

	@staticmethod
	def verify_hash(password, hash):
		return sha256.verify(password, hash)

# Model to revoke jti (json token identifier) 
class RevokedTokenModel(db.Model):
	__tablename__ = 'revoked_tokens'
	id = db.Column(db.Integer, primary_key = True)
	jti = db.Column(db.String(120))
	
	def add(self):
		db.session.add(self)
		db.session.commit()
	
	@classmethod
	def is_jti_blacklisted(cls, jti):
		query = cls.query.filter_by(jti = jti).first()
		return bool(query)
