
import argparse
import os

from kseParser import parseKseProtocol
from smartNetParser import parseSmartNetProtocol

	
def main():
	parser = argparse.ArgumentParser(description='Parse file name')
	parser.add_argument('File', metavar='MyFile', nargs='+',
					help='file with CAN log')
	
	arg = parser.parse_args()
	FileToParse = arg.File[0]
	
	pre, ext = os.path.splitext(FileToParse)
	
	OutputFile = pre + '_out' + ext
	
	with open(FileToParse, 'r') as Input: content = Input.readlines()
	
	if True:
		parseSmartNetProtocol(content, OutputFile)
	else:
		parseKseProtocol(content, OutputFile)
	
	
	print('Done')
	
	
if __name__ == "__main__":
	main()
	