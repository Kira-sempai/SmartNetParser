
import argparse
import os

from kseParser import parseKseProtocol
from smartNetParser import parseSmartNetProtocol

	
def initParser():
	parser = argparse.ArgumentParser(
		description='Parse CAN bus log',
		epilog='If any questions - ask Andreyka'
		)
	
	parser.add_argument('File', metavar='MyFile', nargs='?', help='file with CAN log')
	parser.add_argument('-p', '--protocol', metavar ='Protocol', nargs ='?', choices = ['smartnet', 'kse'], default ='smartnet', help = 'Select protocol to parse')
	parser.add_argument('-i', '--id', metavar ='busId', type = int, nargs ='?', default = -1, help = 'Select bus Id to parse')

	return parser
	
def main():
	parser = initParser()
	arg = parser.parse_args()
	
	FileToParse = arg.File
	
	pre, ext = os.path.splitext(FileToParse)
	
	OutputFile = pre + '_out' + ext
	
	with open(FileToParse, 'r') as Input: content = Input.readlines()
	
	if arg.protocol == 'smartnet':
		parseSmartNetProtocol(content, OutputFile)
	else:
		busId = arg.id
		parseKseProtocol(content, OutputFile, busId)
	
	
	print('Done')
	
	
if __name__ == "__main__":
	main()
	