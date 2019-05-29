#!/usr/bin/env python3
# fmpeg -i input.mp4 -s 320x240 output.mp4
# pip3 install ffmpeg-python
import ffmpeg
import sys
import subprocess
import os
import filetype
from pymediainfo import MediaInfo

resolution_types = [
	["4K", "3840", "2160"],
	["1080p" ,"1080", "1920"],
	["720p", "1280", "720"],
	["480p", "480", "720"],
	["360p", "640", "360"],
	["240p", "426", "240"]
]

def is_video(imported_file):
	media_info = MediaInfo.parse(imported_file)
	for track in media_info.tracks:
		if track.track_type == 'Video':
			return True
	return False

def is_mp4(video):
	type_of_file = filetype.guess(video)

	if type_of_file is None:
		print("Cannot guess filetype")
		return False
	
	print(type_of_file.extension)
	if type_of_file.extension is "mp4":
		return True
	else :
		return False

def convert_to_mp4(vid_input):
	FNULL = open(os.devnull, 'w')
	
	# should replace extension to mp4
	vid_output = vid_input
	vid_output = vid_output.replace(vid_output.split('.')[-1], "mp4")
	print("convert to mp4")
	try :
		p = subprocess.Popen(['ffmpeg', '-i', vid_input, vid_output, '-y'], stdout=FNULL, stderr=FNULL)
		p.wait()
	except:
		print("error")
		sys.exit(1)

	return vid_output

def do_encode(vid_input, width, height):
	encoding = width + "x" + height
	vid_output = str(encoding) + "_" + vid_input

	# don't print anything to stdout nor sterr
	FNULL = open(os.devnull, 'w')

	# -n stand for : not overwrite output files in non-interactive mode
	# put -y for overwriting
	try :
		p = subprocess.Popen(['ffmpeg', '-i', vid_input, '-s', encoding, vid_output, '-n']) #, stdout=FNULL, stderr=FNULL)
		p.wait()
	except:
		print("error")
		sys.exit(1)

def get_video_res(video):
	try:
		probe = ffmpeg.probe(sys.argv[1])
	except ffmpeg.Error as e:
		print(e.stderr, file=sys.stderr)
		sys.exit(1)

	video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
 
	if video_stream is None:
		print('No video stream found', file=sys.stderr)
		sys.exit(1)

	width = int(video_stream['width'])
	height = int(video_stream['height'])
	return width, height

def set_resolution(video):
	width, height = get_video_res(video)
	video_res = width * height
	print(width, height)
	for i in range(len(resolution_types)) :
		resolution = int(resolution_types[i][1]) * int(resolution_types[i][2])
		if resolution < video_res:
			print("encoding in %s" % resolution_types[i][0])
			do_encode(video, resolution_types[i][1], resolution_types[i][2])

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("usage : %s [video]" % sys.argv[0])
		sys.exit(1)

	video = sys.argv[1]
	
	if is_video(video) is False:
		print("file is not video")
		sys.exit(1)
	else :
		print("is vid gr8")

	if is_mp4(video) is False:
		print("not mp4")
		video = convert_to_mp4(video)
		print(video)

	print("set res")
	set_resolution(video)
