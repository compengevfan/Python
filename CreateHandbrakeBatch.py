import argparse
import string
import os
import getpass

def getargs():
	parser = argparse.ArgumentParser
	parser.add_argument('-s','--SeriesName', required=True, action='store')
	parser.add_argument('-n','--SeasonNumber', required=True, action='store')
	parser.add_argument('-p','--SeasonPath', required=True, action='store')
	args = parser.parse_args()
	return args

def main():
	args = getargs()
	
	BeginCommand = '"c:\Program Files\Handbrake\HandBrakeCLI" -Z "Normal" --no-dvdnav -i'
	EndCommand = '.mp4" -m -a "1" -s "scan"'

	EpisodeNumber=1