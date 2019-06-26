from youtube import db, app
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
	def update_user_by_id(cls, data_user):
		user = cls.query.filter_by(id=data_user.id).first()
		user.username = data_user.username
		user.pseudo = data_user.pseudo
		user.email = data_user.email
		user.password = data_user.password
		db.session.commit()

	@classmethod
	def get_user_by_username(cls, username):
		return cls.query.filter_by(username = username).first()

	@classmethod
	def get_user_by_email(cls, email):
		return cls.query.filter_by(email = email).first()

	@classmethod
	def get_user_by_id(cls, id):
		return cls.query.filter_by(id = id).first()

	@classmethod
	def delete_user_by_id(cls, id):
		result = cls.query.filter_by(id = id).delete()
		db.session.commit()
		return result

	@classmethod
	def get_all_users(cls, pseudo):
		if pseudo is None:
			pseudo = ""
		return cls.query.filter(UserModel.pseudo.like('%'+pseudo+'%')).all()

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

class VideoModel(db.Model):
	__tablename__ = 'video'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(45), nullable = False)
	duration = db.Column(db.Integer, nullable = True)
	user_id = db.Column(db.Integer, nullable = False)
	source = db.Column(db.String(200), nullable = False)
	created_at = db.Column(db.Date, nullable = False)
	view = db.Column(db.Integer, nullable = False)
	enabled = db.Column(db.Integer, nullable = False)

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def return_all(cls):
		def to_json(x):
			return {
				"name" : x.name,
				"id" : x.id,
				"source" : x.source,
				"created_at" : str(x.created_at),
				"view" : x.view,
				"enabled" : x.enabled,
				"user" : x.user_id,
				"format" : {
					"1080" : app.config['VIDEO_URL'] + x.name
				}
			}
		return list(map(lambda x: to_json(x), VideoModel.query.all()))


	@classmethod
	def get_video_by_id(cls, id):
		return cls.query.filter_by(id = id).first()

	@classmethod
	def delete_video_by_id(cls, id):
		result = cls.query.filter_by(id = id).delete()
		db.session.commit()
		return result


class CommentModel(db.Model):
	__tablename__ = 'comment'

	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(120), nullable = False)
	user_id = db.Column(db.Integer, nullable = False)
	video_id = db.Column(db.Integer, nullable = False)

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def get_comment_by_id(cls, id):
		return cls.query.filter_by(id = id).first()

	@classmethod
	def get_all_comments_by_user_id(cls, user_id):
		return cls.query.filter_by(user_id = user_id)

	@classmethod
	def get_all_comments_by_video_id(cls, video_id):
		return cls.query.filter_by(video_id = video_id)
