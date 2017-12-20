from prettytable import PrettyTable
import argparse
import constants

def splitAt(w,n):
	list = []
	for i in range(0,len(w),n):
		list.append(w[i:i+n])
	return list

def cutFromLine(line, n):
	if not n: return '', line
	return line[:n], line[n:]

def getHeaderLen(headerType):
	CANHeaderIDE = {
		't': 'STANDARD',
		'T': 'EXTENDED',
	}
	
	if headerType not in CANHeaderIDE: return
	
	IDE = CANHeaderIDE[headerType]
	if   IDE == 'STANDARD': return 4
	elif IDE == 'EXTENDED': return 8

def prepareTable():
	t = PrettyTable([	'T',
						'dT',
						'Header',
						'Flag',
						'Func',
						'ID',
						'Type',
						'Body',
						'Parsed header',
						'Parsed body'
					])
	t.align = 'r'
	t.align['Body'] = 'l'
	return t

def parseCANUSBLine(line):
	headerType, line = cutFromLine(line, 1)
	headerLen = getHeaderLen(headerType)
	if headerLen != 8: return None, None, None
	
	header, line = cutFromLine(line, headerLen)
	header = splitAt(header, 2)
	
	bodySize, line = cutFromLine(line, 1)
	bodySize = int(bodySize, 16)
	body, line = cutFromLine(line, bodySize * 2)
	body = splitAt(body, 2)
	timestamp, line = cutFromLine(line, 4)
	
	return header, body, int(timestamp, 16)

def parseHeader(header):
	if len(header) != 4: return None, None, None, None

	flag    = header[0][0]
	reserve = header[0][1]
	function= header[1]
	id      = header[2]
	type    = header[3]

	return (
		int(flag, 16),
		int(function, 16),
		int(id  , 16),
		int(type, 16)
	)
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Parse file name')
	parser.add_argument('File', metavar='MyFile', nargs='+',
					help='file with CAN log')
	
	arg = parser.parse_args()
	FileToParse = arg.File[0]
	
	with open(FileToParse, 'r') as Input: content = Input.readlines()
	
	t = prepareTable()
	
	oldTimestamp = 0
	
	for line in content:
		header, body, timestamp = parseCANUSBLine(line)
		if not header: continue
		
		(	headerFlag,
			headerFunction,
			headerID,
			headerType
		) = parseHeader(header)
		
		if headerFlag == None: continue
		
		headerStr = ' '.join(header)
		bodyStr   = ' '.join(body)
		
		delta = timestamp - oldTimestamp
		oldTimestamp = timestamp
		
		t.add_row([	timestamp,
					delta,
					headerStr,
					headerFlag,
					headerFunction,
					headerID,
					headerType,
					bodyStr,
					'TODO',
					'TODO'
				])
	
	with open('Output.txt', 'w') as Output: Output.write(t.get_string())
	
	print 'Done'