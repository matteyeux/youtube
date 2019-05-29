#!/usr/bin/env python3
# fmpeg -i input.mp4 -s 320x240 output.mp4
# pip3 install ffmpeg-python
import ffmpeg
import sys
import subprocess
import os

resolution_types = [
	["4K", "3840", "2160"],
	["1080p" ,"1080", "1920"],
	["720p", "1280", "720"],
	["480p", "480", "720"],
	["360p", "640", "360"],
	["240p", "426", "240"]
]

def do_encode(vid_input, width, height):
	encoding = width + "x" + height
	vid_output = str(encoding) + "_" + vid_input

	# don't print anything to stdout nor sterr
	FNULL = open(os.devnull, 'w')

	# -n stand for : not overwrite output files in non-interactive mode
	# put -y for overwriting
	try :
		p = subprocess.Popen(['ffmpeg', '-i', vid_input, '-s', encoding, vid_output, '-n'], stdout=FNULL, stderr=FNULL)
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

	for i in range(len(resolution_types)) :
		resolution = int(resolution_types[i][1]) * int(resolution_types[i][2])
		if resolution < video_res:
			print("encoding in %s" % resolution_types[i][0])
			do_encode(video, resolution_types[i][1], resolution_types[i][2])

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("usage : %s [video]" % sys.argv[1])
		sys.exit(1)

	set_resolution(sys.argv[1])
