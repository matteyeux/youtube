#!/usr/bin/env python3
# fmpeg -i input.mp4 -s 320x240 output.mp4
# pip3 install ffmpeg-python

import ffmpeg
import sys
import subprocess
import os
import magic

resolution_types = [
	["4K", "3840", "2160"],
	["1080p" ,"1080", "1920"],
	["720p", "1280", "720"],
	["480p", "480", "720"],
	["360p", "640", "360"],
	["240p", "426", "240"]
]

def is_video(imported_file):
	with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
		if m.id_filename(imported_file).split('/')[0] == "video" :
			return True
	return False

def is_mp4(video):
	with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
		if m.id_filename(video).split('/')[1] == "mp4" :
			return True
	return False

def convert_to_mp4(vid_input):
	FNULL = open(os.devnull, 'w')

	# replace extension to mp4
	vid_output = vid_input
	vid_output = vid_output.replace(vid_output.split('.')[-1], "mp4")
	print("[i] converting %s to %s" % (vid_input, vid_output))

	# create ffmpeg subprocess and wait for it
	try :
		p = subprocess.Popen(['ffmpeg', '-i', vid_input, vid_output, '-y'], stdout=FNULL, stderr=FNULL)
		p.wait()
	except:
		print("[e] ffmpeg failed")
		sys.exit(1)

	return vid_output

# encode video to a lower resolution
def do_encode(vid_input, resolution_type):
	resolution = resolution_type[0]
	encoding = resolution_type[1] + "x" + resolution_type[2]
	video_name = vid_input.split('/')[-1].split('.')[0]

	vid_output = "../../newFront/myyoutubeapp/assets/videos/" + video_name + "/" + resolution + ".mp4"

	# don't print anything to stdout and sterr
	FNULL = open(os.devnull, 'w')

	# -n stands for : not overwrite output files in non-interactive mode
	# put -y for overwriting
	try :
		p = subprocess.Popen(['ffmpeg', '-i', vid_input, '-s', encoding, vid_output, '-n'], stdout=FNULL, stderr=FNULL)
		p.wait()
	except:
		print("[e] error")
		sys.exit(1)

# get max resolution of video
def get_video_res(video):
	try:
		probe = ffmpeg.probe(video)
	except ffmpeg.Error as e:
		sys.exit(1)

	video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
 
	if video_stream is None:
		sys.exit(1)

	width = int(video_stream['width'])
	height = int(video_stream['height'])
	return width, height

def set_resolution(video):
	width, height = get_video_res(video)
	video_res = width * height

	# parse dictionary to get max resolution to use
	for i in range(len(resolution_types)) :
		resolution = int(resolution_types[i][1]) * int(resolution_types[i][2])
		if resolution < video_res:
			print("[x] encoding in %s" % resolution_types[i][0])
			do_encode(video, resolution_types[i])

# aim of this function is to move default video
# to it's new folder
# uploads/18.mp4 -> video/18/1080p/1080p.mp4
def put_video_in_folder(video):
	# get width and height of video
	height, width = get_video_res(video)
	video_name = video.split('/')[-1].split('.')[0]

	# compare with dictionary
	for i in range(0, len(resolution_types)):
		if resolution_types[i][1] == str(width) and resolution_types[i][2] == str(height):
			folder = "video/" + video_name

			# move video the right directory. eg: video/18/1080p/1080p.mp4
			os.rename(video, folder + "/" + resolution_types[i][0] + ".mp4")

if __name__ == '__main__':
	for video in os.listdir("../../newFront/myyoutubeapp/assets/uploads/"):
		if video != ".keep":
			video_path = "../../newFront/myyoutubeapp/assets/uploads/" + video
			new_dir = "../../newFront/myyoutubeapp/assets/videos/" + video.split('.')[0]

			try:
				print("[i] creating dir %s" % new_dir)
				os.mkdir(new_dir)
			except:
				pass

			if is_video(video_path) is False:
				print("[e] file is not video")
				sys.exit(1)

			if is_mp4(video_path) is False:
				video = convert_to_mp4(video_path)

			set_resolution(video_path)
			put_video_in_folder(video_path)
