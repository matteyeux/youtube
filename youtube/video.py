from flask_restful import Resource, reqparse, request
from models import UserModel, RevokedTokenModel, VideoModel
from werkzeug.utils import secure_filename
from youtube import app
import datetime, os

parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)

class VideoCreate(Resource):
	def post(self):
		data = parser.parse_args()

		new_video = VideoModel(
			name = data["name"],
			duration = 0,
			user_id = 25,
			source = "ppfffrtrt",
			created_at = datetime.datetime.now(),
			view = 1,
			enabled = False
		)

		try:
			new_video.save_to_db()
			VideoCreate.import_data(self, request.files['source'])
			return {
				'message': 'OK',
				'data': {
					'video': "video",
				}
			}, 201
		except:
			return {'message': 'Something went wrong'}, 400

	# Import video file into the server
	def import_data(self, file):
		try:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['VIDEO_FOLDER'], filename))
			url = os.path.join(app.config['VIDEO_URL'], filename)
			self.image_filename = filename
		except:
			return {'message': 'Something went wrong'}, 400
		return self

class AllVideos(Resource):
	def get(self):
		return VideoModel.return_all()

# video check 
# fileInfo = MediaInfo.parse('some/file/name.ext')
# for track in fileInfo.tracks:
#     if track.track_type == "Video":
#         # success!