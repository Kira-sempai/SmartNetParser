try:
	from prettytable import PrettyTable
except ImportError:
	print('PrettyTable module not installed\nSee https://pypi.org/project/prettytable/\n')
	exit()

from commonParser import parseCANUSBLineCommon
import constantsKse



def parseKseHeader(header):
	header = int(header[0] + header[1], 16)
	
	module = (header >> 7) & 0x0F
	busId  = (header & 0x7F)
	
	return module, busId
	
def getKseModuleNameId(module, busId):
	moduleName = constantsKse.kseModule.get(module, 'None')
	return '{} ({})'.format(moduleName, busId)
	
def getKseFuntionName(body):
	functionCodeSize = 3 if body[2] == 'FA' else 1
	if functionCodeSize == 1:
		if body[2] == '0E':
			value = int(body[3] + body[4], 16)
			if value == 0x8000:
				temperatureValue = 'Undefined'
			else:
				temperatureValue = '%0.1f' % (value/10.0)
			 
			return 'DHW Temperature = %s' %(temperatureValue)
		
	return 'Undefined'
	
def getKseBodyDescription(body):
	destModule   = int(body[0][0], 16)
	messageType  = int(body[0][1], 16)
	destModuleId = int(body[1]   , 16)
	
	functionName = getKseFuntionName(body)
	
	toModule = getKseModuleNameId(destModule, destModuleId)
	messageTypeStr = 'request' if messageType == 1 else 'response'
	return ('to ' + toModule +
		messageTypeStr + ' ' +
		functionName)
	

def prepareKseTable():
	t = PrettyTable([	'T',
						'dT',
						'MT',
						'Header',
						'Body',
						'Parsed header',
						'Parsed body'
					])
	t.align = 'r'
	t.align['Body'] = 'l'
	return t
	

def parseKseProtocolLine(line, t):
	parseKseProtocolLine.i += 1
	
	try:
		pLine = parseCANUSBLineCommon(line)
	except:
		print('Line %d: %s fail' %(parseKseProtocolLine.i, line))
		return
	
	if pLine['messageType'] != 't':
		return
	
	body      = pLine['body']
	timestamp = pLine['timestamp']
	header    = pLine['header']
	delta     = pLine['deltaT']
	
	module, busId = parseKseHeader(header)
	
	parsedHeader = getKseModuleNameId(module, busId)
	parsedBody   = getKseBodyDescription(body)
	
	headerStr = ' '.join(header)
	bodyStr   = ' '.join(body)
	
	t.add_row([	timestamp,
				delta,
				pLine['messageType'],
				headerStr,
				bodyStr,
				parsedHeader,
				parsedBody
			])
	
#init static var
parseKseProtocolLine.i         = 0

def parseKseProtocol(content, outputFile):
	t = prepareKseTable()
	for line in content:
		parseKseProtocolLine(line, t)
	
	with open(outputFile, 'w') as Output: Output.write(t.get_string())
