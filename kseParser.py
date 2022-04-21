from asyncio import streams
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
		
	return ' '

def getParameterId(body):
	if body[0] == 'FA':
		return int(body[1] + body[2], 16)

	return int(body[0], 16)
	

def getParameterName(parameterId):
	if parameterId in constantsKse.kseParameter:
		return constantsKse.kseParameter[parameterId]['name']
	
	return '0x%X' % (parameterId)

def getTemperatureValue(body):
	value = int(body[0] + body[1], 16)
	if value == 0x8000:
		return 'Undefined'
	if value == 0xFE70:
		return 'Unused'

	return '%0.1f' % (value/10.0)

def getU8Value(body):
	value = int(body[0], 16)
	return '%d' % (value)

def getBitValue(body):
	value = int(body[0], 16)
	return '0' if value == 0 else '1' 

def getParameterValue(parameterId, body):
	if parameterId in constantsKse.kseParameter:
		if constantsKse.kseParameter[parameterId]['format'] == 'temperature':
			return getTemperatureValue(body)
		if constantsKse.kseParameter[parameterId]['format'] == 'u8':
			return getU8Value(body)
		if constantsKse.kseParameter[parameterId]['format'] == 'bit':
			return getBitValue(body)
	
	return int(''.join(body), 16)

def getKseBodyFormattedValue(parsedBody):
	
	parameterName  = getParameterName(parsedBody['parameter'])
	messageType    = parsedBody['messageType']
	toModule       = getKseModuleNameId(parsedBody['module'], parsedBody['id'])
	
	str = f'to {toModule:<15} {messageType}: {parameterName}'
	
	if messageType == 'req':
		return str
	
	parameterValue = parsedBody['value']
	
	return f'{str} = {parameterValue}'

def parseKseBody(body):
	destModule   = int(body[0][0], 16)
	messageType  = int(body[0][1], 16)
	destModuleId = int(body[1]   , 16) & 0x0F
	valuePos = 5 if body[2] == 'FA' else 3
	
	parameterId    = getParameterId   (body[2:])
	parameterValue = getParameterValue(parameterId, body[valuePos:valuePos+2])
	
	messageTypeStr = 'req' if messageType == 1 else 'res'
	return {
		'messageType': messageTypeStr,
		'module'     : destModule,
		'id'         : destModuleId, 
		'parameter'  : parameterId,
		'value'      : parameterValue,
		}

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
	t.align['Parsed body'] = 'l'
	return t
	

def parseKseProtocolLine(line, t, filterBusId):
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
	parsedBody    = parseKseBody(body)
	
	if filterBusId != -1:
		if (busId != filterBusId) and parsedBody['id'] != filterBusId:
			return
	
	formattedHeader = getKseModuleNameId(module, busId)
	formattedBody   = getKseBodyFormattedValue(parsedBody)
	
	headerStr = ' '.join(header)
	bodyStr   = ' '.join(body)
	
	t.add_row([	timestamp,
				delta,
				pLine['messageType'],
				headerStr,
				bodyStr,
				formattedHeader,
				formattedBody
			])
	
#init static var
parseKseProtocolLine.i = 0

def parseKseProtocol(content, outputFile, busId):
	t = prepareKseTable()
	for line in content:
		parseKseProtocolLine(line, t, busId)
	
	with open(outputFile, 'w') as Output: Output.write(t.get_string())
