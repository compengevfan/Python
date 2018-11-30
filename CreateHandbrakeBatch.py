import argparse
import string
import os
import getpass

def getargs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', required=True, action='store') #Series Name
	parser.add_argument('-n', required=True, action='store') #Season Number
	parser.add_argument('-p', required=True, action='store') #Season Path
	args = parser.parse_args()
	return args

def toUnix(path):
    return path.replace("\\", "/")

def main():
	args = getargs()
	
	BeginCommand = '"c:\Program Files\Handbrake\HandBrakeCLI" -Z "Roku 720p30 Surround" --no-dvdnav -i'
	EndCommand = '.mp4" -m -a "1" -s "scan"'
	
	BatchFileOutput = ""

	UnixPath = toUnix(args.p)

	disks = os.listdir(UnixPath)
	disks.sort()
	for disk in disks:
		print "Processing disk: " + disk
		EpisodeCount = input("How many episodes on this disk? ")

		while EpisodeCount != 0:
			EpisodeNumber = input("Episode number: ")
			Title = input("Title number for episode " + str(EpisodeNumber) + ": ")
			InputLocation = '"' + args.p + "\\" + disk + '" -t'
			OutputLocation = '-o "\\\storage1\media\TV Shows\\' + args.s + "\Season " + args.n + "\\" + args.s + " - s" + args.n + "e" + str(EpisodeNumber)
			BatchFileOutput += BeginCommand + " " + InputLocation + " " + str(Title) + " " + OutputLocation + EndCommand + "\n"
			
			#print BatchFileOutput
			
			EpisodeCount -= 1
		print "Going to next disk..."
		
	
		
	if not os.access("C:\Cloud\Dropbox\EpisodeTracker\\" + args.s, os.F_OK):
		os.mkdir("C:\Cloud\Dropbox\EpisodeTracker\\" + args.s)
	
	BatFile = open("C:\Cloud\Dropbox\EpisodeTracker\\" + args.s + "\Season " + args.n + ".bat", "w")
	BatFile.write(BatchFileOutput)
	BatFile.close()

if __name__ == "__main__":
        main()
