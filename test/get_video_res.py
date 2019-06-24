#!/usr/bin/env python3
import ffmpeg
import sys

if __name__ == '__main__':
	for i in range(1, len(sys.argv)):
		try:
			probe = ffmpeg.probe(sys.argv[i])
		except ffmpeg.Error as e:
			print(e.stderr, file=sys.stderr)
			sys.exit(1)

		video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
	
		if video_stream is None:
			print('No video stream found', file=sys.stderr)
			sys.exit(1)

		width = int(video_stream['width'])
		height = int(video_stream['height'])
		print("=== %s ===" % sys.argv[i])
		print("width: %s" % width)
		print("height: %s" % height)

