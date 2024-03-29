import sys
sys.path.insert(0, "../../encoder/src")
sys.path.insert(0, "../../search_engine")
import encoder
import algolia

from pymediainfo import MediaInfo
from flask_restful import Resource, reqparse, request
from models import UserModel, RevokedTokenModel, VideoModel
from werkzeug.utils import secure_filename
from youtube import app
from resources import is_authentified, actual_user_id, is_user_connected, paging, number_page
from user import is_user_connected
import datetime, os

parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)

class VideoCreate(Resource):
	def post(self):
		data = parser.parse_args()

		if is_authentified() is None:
			return {"message": "Unauthorized"}, 401

		user_id = actual_user_id()

		if VideoCreate.import_data(self, request.files['source']) is None:
			return {'message': 'Bad Request', 'code' : 2001, 'data' : 'Not a video'}, 400
		try:
			new_video = VideoModel(
				name = data["name"],
				duration = 0,
				user_id = user_id,
				source = app.config['VIDEO_FOLDER'] + data["name"],
				created_at = datetime.datetime.now(),
				view = 0,
				enabled = True
			)

			data_user = UserModel.get_user_by_id(user_id)
			new_video.save_to_db()

			with open('../../newFront/myyoutubeapp/assets/uploads/mail', 'w') as f:
				f.write(data_user.email)

			with open('../../newFront/myyoutubeapp/assets/uploads/name', 'w') as f:
				f.write(data["name"])	

			# print('algolia')
			# algolia.send_data_to_algolia()

			return {
				'message': 'OK',
				'data': {
					'video': "video"
				}
			}, 201
		except:
			return {'message': 'Bad Request', 'code' : 2002, 'data' : 'failed to save video'}, 400

	# Import video file into the server
	def import_data(self, file):
		try:
			if file.content_type.split('/')[0] != "video":
				print("none : %s" % file.content_type.split('/')[0])
				return None
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['VIDEO_FOLDER'], filename))
			self.image_filename = filename
		except:
			return {'message': 'Bad Request', 'code' : 2003, 'data' : 'failed to import video'}, 400
		return self

class AllVideos(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('page', help='This field cannot be blank', required=False)
		parser.add_argument('perPage', help='This field cannot be blank', required=False)
		json = parser.parse_args()

		datum = VideoModel.return_all()
		page = json['page']
		perPage = json['perPage']

		if page is None:
			page = 1
		if perPage is None:
			perPage = 100

		results = paging(datum, int(page), int(perPage))
		total_page = number_page(datum, int(perPage))

		if results:
			return { 
				'message': 'OK', 
				'data': results,
				'pager': {
					'current': page,
					'total': total_page
					}
				}, 200
		else:
			return { 'message': 'Not found'}, 404

class Video(Resource):
	def get(self, id):
		# parser = reqparse.RequestParser()
		# json = parser.parse_args()

		result = VideoModel.get_video_by_id(id)

		if result:
			data = {
				'id': result.id,
				'name': result.name,
				'source': result.source,
				'created_at': str(result.created_at),
				'view': result.view,
				'enabled': result.enabled,
				'user': result.id
			}
			return {'message': 'OK', 'data': data}
		else:
			return {'message': 'Not found'}, 404

class VideoDelete(Resource):
	def delete(self, id):
		if is_authentified()!=True:
			return {"message": "Unauthorized"}, 401
		result = VideoModel.get_video_by_id(id)
		if result:
			if result and is_user_connected(result.user_id):
				VideoModel.delete_video_by_id(id)
				return 204
			else:
				return {"message": "Forbidden"}, 403
		else:
			return {'message': 'Not found'}, 404

def is_video(imported_file):
	media_info = MediaInfo.parse(imported_file)
	for track in media_info.tracks:
		if track.track_type == 'Video':
			return True
	return False
