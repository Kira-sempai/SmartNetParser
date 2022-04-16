try:
	from prettytable import PrettyTable
except ImportError:
	print('PrettyTable module not installed\nSee https://pypi.org/project/prettytable/\n')
	exit()

from commonParser import parseCANUSBLineCommon
import constantsKse


def parseKseCANUSBLine(line):
	return parseCANUSBLineCommon(line)
	


def parseKseHeader(header):
	header = int(header, 16)
	
	module = (header >> 7) & 0x0F
	busId  = (header & 0x7F)
	
	return module, busId
	
def getKseModuleName(module):
    return constantsKse.kseModule.get(module, 'None')    # 5 is default if module not found
	
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
	

def prepareKseTable():
	t = PrettyTable([	'T',
						'dT',
						'MT',
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
	
	
def parseKseProtocol(content, outputFile):
	t = prepareKseTable()
	oldTimestamp = 0
	for line in content:
		pLine = parseKseCANUSBLine(line)
		
		if pLine['messageType'] != 't':
			continue
		
		body      = pLine['body']
		timestamp = pLine['timestamp']
		
		module, busId = parseKseHeader(pLine['header'])
		
		bodyStr   = ' '.join(body)
		
		delta = timestamp - oldTimestamp
		oldTimestamp = timestamp
		
		parsedHeader = getKseModuleName(module)
		parsedBody   = getKseBodyDescription(body)
		
		t.add_row([	timestamp,
					delta,
					pLine['messageType'],
					pLine['header'],
					format(module, '#04x'),
					busId,
					bodyStr,
					parsedHeader,
					parsedBody
				])
	
	with open(outputFile, 'w') as Output: Output.write(t.get_string())
