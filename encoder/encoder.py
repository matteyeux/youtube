#!/usr/bin/env python3
# fmpeg -i input.mp4 -s 320x240 output.mp4
# pip3 install ffmpeg-python
from __future__ import unicode_literals, print_function
import argparse
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
	
	FNULL = open(os.devnull, 'w')

	try :
		p = subprocess.Popen(['ffmpeg', '-i', vid_input, '-s', encoding, vid_output], stdout=FNULL)
	except:
			print("error")
			sys.exit(1)

if __name__ == '__main__':
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
	video_res = width * height

	print("width: %s" % width)
	print("height: %s" % height)

	for i in range(len(resolution_types)) :
		resolution = int(resolution_types[i][1]) * int(resolution_types[i][2])
		if  resolution < video_res:
			print("encode in : %s" % resolution_types[i][0])
			do_encode(sys.argv[1], resolution_types[i][1], resolution_types[i][2])
	
