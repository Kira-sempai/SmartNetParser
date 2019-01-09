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
	if   IDE == 'STANDARD': return 3
	elif IDE == 'EXTENDED': return 8

def prepareSmartNetTable():
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

def parseSmartNetCANUSBLine(line):
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

def parseSmartNetHeader(header):
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
	
def parseSmartNetProtocol(content):
	t = prepareSmartNetTable()

	oldTimestamp = 0
	for line in content:
		header, body, timestamp = parseSmartNetCANUSBLine(line)
		if not header: continue
		
		(	headerFlag,
			headerFunction,
			headerID,
			headerType
		) = parseSmartNetHeader(header)
		
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
	
	
def prepareKseTable():
	t = PrettyTable([	'T',
						'dT',
						'Header',
						'module',
						'busId',
						'Body',
						'Parsed header',
						'Parsed body'
					])
	t.align = 'r'
	t.align['Body'] = 'l'
	return t
	
def parseKseCANUSBLine(line):
	headerType, line = cutFromLine(line, 1)
	headerLen = getHeaderLen(headerType)
	
	if headerLen != 3: return None, None, None
	
	header, line = cutFromLine(line, headerLen)
	
	bodySize, line = cutFromLine(line, 1)
	bodySize = int(bodySize, 16)
	body, line = cutFromLine(line, bodySize * 2)
	body = splitAt(body, 2)
	timestamp, line = cutFromLine(line, 4)
	
	return header, body, int(timestamp, 16)

	
def parseKseHeader(header):
	header = int(header, 16)
	
	module = (header >> 7) & 0x0F
	busId  = (header & 0x7F)
	
	return module, busId
	
def getKseModuleName(module):
    return {
        0x03: 'Kessel'   ,
        0x06: 'Bedien'   ,
        0x09: 'Manager'  ,
        0x0A: 'Heizmodul',
        0x0C: 'Mischer'  ,
		0x0D: 'CoCo'     ,
    }.get(module, 'None')    # 5 is default if module not found
	
def getKseFuntionName(body):
	functionCodeSize = 3 if body[2] == 'FA' else 1
	if functionCodeSize == 1:
		if body[2] == '0E': return 'DHW Temperature'
		
	return 'Undefined'
	
def getKseBodyDescription(body):
	destModule  = int(body[0][0], 16)
	messageType = int(body[0][1], 16)
	destModuleId = body[1]
	functionName = getKseFuntionName(body)
	
	toModule = getKseModuleName(destModule)
	messageTypeStr = 'request' if messageType == 1 else 'response'
	return ('to ' + toModule + ' (' + destModuleId + ') ' +
		messageTypeStr + ' ' +
		functionName)
	
	
def parseKseProtocol(content):
	t = prepareKseTable()
	oldTimestamp = 0
	for line in content:
		header, body, timestamp = parseKseCANUSBLine(line)
		if not header: continue
		
		module, busId = parseKseHeader(header)
		
		bodyStr   = ' '.join(body)
		
		delta = timestamp - oldTimestamp
		oldTimestamp = timestamp
		
		parsedHeader = getKseModuleName(module)
		parsedBody   = getKseBodyDescription(body)
		
		t.add_row([	timestamp,
					delta,
					header,
					format(module, '#04x'),
					busId,
					bodyStr,
					parsedHeader,
					parsedBody
				])
	
	with open('Output.txt', 'w') as Output: Output.write(t.get_string())


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Parse file name')
	parser.add_argument('File', metavar='MyFile', nargs='+',
					help='file with CAN log')
	
	arg = parser.parse_args()
	FileToParse = arg.File[0]
	
	with open(FileToParse, 'r') as Input: content = Input.readlines()
	
	if False:
		parseSmartNetProtocol(content)
	else:
		parseKseProtocol(content)
	
	
	print 'Done'