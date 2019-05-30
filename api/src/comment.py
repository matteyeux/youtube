from flask_restful import Resource, reqparse, request
from models import UserModel, TokenModel, RevokedTokenModel, CommentModel
from resources import is_authentified, actual_user_id, is_user_connected
import datetime

parser = reqparse.RequestParser()
parser.add_argument('body', help = 'This field cannot be blank', required = True)
parser.add_argument('user_id', help = 'This field cannot be blank', required = False)
parser.add_argument('video_id', help = 'This field cannot be blank', required = False)


class Comment(Resource):
	def post(self, id):
		data = parser.parse_args()
		user_id = actual_user_id()
		# video_exist = get_videos_by_id(id)

		if is_authentified()!=True:
			return {"message": "Unauthorized"}, 401

		result = UserModel.get_user_by_id(user_id)

		if result and is_user_connected(user_id):
			# TODO : Rajouter une condition pour check que la vidéo existe
			new_comment = CommentModel(
				body = data['body'],
				user_id = user_id,
				video_id = id
			)
			try:
				new_comment.save_to_db()
				return {
					'message': 'OK',
					'data': data['body']
				}, 201
			except:
				return {
					'message': 'Bad Request',
					'code': '1001 => User {} already exists'. format(data['username']),
					'data': {
						'username': current_user.username,
						'pseudo': current_user.pseudo,
						'email': current_user.email
						}
					}, 400

# List all users
class GetAllComments(Resource):
	def get(self, video_id):
		result = CommentModel.get_all_comments_by_video_id(video_id)
		datum = []
		for data in result:
			datum.append({
				'id': data.id,
				'body': data.body,
				'user_id': data.user_id,
			})
		if datum:
			return { 'message': 'OK', 'data': datum }
		else:
			return { 'message': 'Not found'}, 404