from pytube import YouTube
from pytube.helpers import safe_filename

import pysubs2

from pydub.playback import play
from pydub import AudioSegment

import sys, os

import argparse
from urllib.parse import parse_qs, urlparse

data_path = "./data"

def ingest_dataset(yt_uri):
	# Use vid as the diretory name for download and processing
	vids = parse_qs(urlparse(yt_uri).query, keep_blank_values=True).get('v')
	vid = None if vids == None else vids[0]

	try:
		# Get information on the YouTube content
		yt = YouTube(yt_uri)

		# Filename for audio stream (.mp4) and subtitle (.srt) files
		audio = vid + '.mp4'
		subtitle = os.path.join(data_path, vid + '.srt')

		# Download subtitle and write to an .srt file
		subtitle_content = yt.captions.get_by_language_code('ko')
		subtitle_file = open(subtitle, 'w')
		subtitle_file.write(subtitle_content.generate_srt_captions())

		# Download audio stream
		# download() auto appends file extension (.mp4)
		yt.streams.filter(only_audio=True, subtype='mp4').first().download(
			output_path=data_path, filename=vid)

	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		exc_file = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, exc_file, exc_tb.tb_lineno)
		sys.exit(1)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument(
		'path', help="URL of the video file to make speech recognition corpus from")

	args = parser.parse_args()

	if args.path.startswith('https://'):
		ingest_dataset(args.path)
	else:
		print("URL of the video file should start with https://")
		sys.exit(1)