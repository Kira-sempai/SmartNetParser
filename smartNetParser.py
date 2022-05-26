try:
	from prettytable import PrettyTable
except ImportError:
	print('PrettyTable module not installed\nSee https://pypi.org/project/prettytable/\n')
	exit()

import json
import datetime
from commonParser import parseCANUSBLineCommon
import constantsSmartNet

def prepareSmartNetTable():
	t = PrettyTable([	'T',
						'dT',
						'MT',
						'Header',
						'Body',
						'Parsed header',
						'Parsed body'
					])
	t.align                  = 'r'
	t.align['Body']          = 'l'
	t.align['Parsed header'] = 'l'
	t.align['Parsed body']   = 'l'
	return t

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

	
class Program(object):
	def __init__(self, id, type):
		self.id   = id
		self.type = type
		
		if (self.type in constantsSmartNet.ProgramType) and (constantsSmartNet.ProgramType[self.type] in constantsSmartNet.Function):
			self.functionDict = constantsSmartNet.Function[constantsSmartNet.ProgramType[self.type]]
		else:
			self.functionDict = None	
		
	
	def getProgramTypeName(self):
		if self.type in constantsSmartNet.ProgramType:
			return constantsSmartNet.ProgramType[self.type]
		
		return 'UNK_Type'
		
	def getFunctionName(self, functionId):
		if self.functionDict and (functionId in self.functionDict):
			return self.functionDict[functionId]
		
		return 'UNK_Func'


def getSmartNetHeaderDescription(id, programTypeId, functionId, flag):
	prg = Program(id, programTypeId)
	
	programTypeName = prg.getProgramTypeName()
	functionName    = prg.getFunctionName(functionId)
	flagName        = constantsSmartNet.smartNetHeaderFlag[flag]
	
	return '{} {}({:3})->{}'.format(flagName[:3], programTypeName, id, functionName)


def parseMappingValue(value):
	host = int(value[0], 16)
	
	channelIdAndType = int(value[1], 16)
	
	channelId = channelIdAndType & 0x1F
	channelType = channelIdAndType >> 5
	
	typeDict = {
		0: 'SENSOR_LOCAL',
		1: 'RELAY_LOCAL',
		2: 'SENSOR',
		3: 'RELAY',
		4: 'INPUT',
		5: 'OUTPUT',
		6: 'RESERVED',
		7: 'UNDEFINED',
	}
	
	return {
		'host': host,
		'id'  : channelId,
		'type': typeDict[channelType]
	}

def smartNetControllerIAmHereDescription(flag, body):
	if flag == 0:
		return ''
	
	try:
		controllerTypeId  = int(body[0], 16)
	except:
		return ''
	
	if len(body) > 1:
		deviceId = int('{}'.format(body[1]), 16)
		
	if len(body) > 2:
		oemId = int('{}'.format(body[2]), 16)
	
	typeDict = constantsSmartNet.ControllerType
	
	if controllerTypeId in typeDict:
		type = typeDict[controllerTypeId]
	else:
		type = 'UNK'
	
	return 'Ctrl Type: ' + type

def smartNetControllerGetRelayMappingDescription(flag, body):
	channelId = int(body[0], 16)
	
	if flag == 0:
		return f'id = {channelId}'
	
	mapping = parseMappingValue(body[1:])
	
	mappingStr = json.dumps(parseMappingValue(body[1:]))
	return f'id = {channelId}: {mappingStr}'
	
def smartNetControllerGetOutputValueBodyDescription(flag, body):
	if flag == 0:
		return ''
	
	mapping = parseMappingValue(body[:2])
	
	if   mapping['type'] == 'OUTPUT':
		value = int(body[2], 16)
	elif mapping['type'] == 'SENSOR':
		value = int(body[2] + body[3], 16)/10.0
	else:
		value = ''
	
	return 'host={:2} channelId={:2} type={:7} value={:5}'.format(mapping['host'], mapping['id'], mapping['type'], value)

def smartNetControllerJournalBodyDescription(flag, body):
	
	if len(body) < 7:
		return ''
			
	operationsDict = {
		0 : 'OP_STATUS'  ,
		1 : 'OP_MESSAGE1',
		2 : 'OP_MESSAGE2',
		3 : 'OP_MESSAGE3',
	}
	
	numAndOperation = int(body[0], 16)
	num       = numAndOperation & 0x1F
	operation = numAndOperation >> 5
	
	if operation in [0, 1]:
		severity = int(body[1], 16)
#		crc16 = int('{}{}'.format(body[3], body[2]), 16)
		crc16 = body[3] + body[2]
		timestamp = int('{}{}{}{}'.format(body[7], body[6], body[5], body[4]), 16)
		messageDateTime = datetime.datetime.utcfromtimestamp(timestamp)
		return 'Op={} N={} DT={} severity={} crc={}'.format(operation, num, messageDateTime, severity, crc16)
	elif operation == 2:
		code = body[1]
		param_ex = '[{} {}]'.format(body[2], body[3])
		param = '[{} {} {} {}]'.format(body[4], body[5], body[6], body[7])
		return 'Op={} N={} Code={} Param={} ParamEx={}'.format(operation, num, code, param, param_ex)
	else:
		param_ex = '[{} {} {} {} {} {}]'.format(body[1], body[2], body[3], body[4], body[5], body[6])
		return 'Op={} N={} ParamEx={}'.format(operation, num, param_ex)
	

def smartNetControllerInitLogTransmitDescription(flag, body):
	startTime = int('{}{}{}{}'.format(body[3], body[2], body[1], body[0]), 16)
	endTime   = int('{}{}{}{}'.format(body[7], body[6], body[5], body[4]), 16)
	
	startTime = datetime.datetime.utcfromtimestamp(startTime)
	endTime   = datetime.datetime.utcfromtimestamp(endTime)
	
	return 'From:{} To:{}'.format(startTime, endTime)
	
def smartNetControllerGetLogPartDescription(flag, body):
	chunkId         = int('{}'.format(body[0]), 16)
	chunkControlInt = int('{}'.format(body[1]), 16)
	
	control = {
	 0xFA: 'CHUNK_PARTS_MAX_NUM',
	 0xFB: 'GET_SIZE',
	 0xFC: 'START_TRANSMIT',
	 0xFD: 'END_TRANSMIT',
	 0xFE: 'CHUNK_NOT_EXIST',
	 0xFF: 'GET_CRC',
	}
	
	if chunkControlInt in control:
		chunkControlStr = control[chunkControlInt]
	else:
		chunkControlStr = str(chunkControlInt)
	
	bodyStartStr = (str(chunkId) + '.' + chunkControlStr)
	
	if constantsSmartNet.smartNetHeaderFlag[flag] == 'Request':
		return (bodyStartStr + '!')
	
	dataSize = 6
	
	if chunkControlStr == 'CHUNK_PARTS_MAX_NUM' : dataSize = 2
	if chunkControlStr == 'GET_SIZE'            : dataSize = 2
	if chunkControlStr == 'START_TRANSMIT'      : dataSize = 0
	if chunkControlStr == 'END_TRANSMIT'        : dataSize = 0
	if chunkControlStr == 'CHUNK_NOT_EXIST'     : dataSize = 0
	if chunkControlStr == 'GET_CRC'             : dataSize = 2
	

	if dataSize > 0:
		data = body[2:]
			
		dataStr = ' '.join(data)
		bodyStr = (': ' + dataStr)
	else:
		bodyStr = '.'
	
	return (bodyStartStr + bodyStr)
	
	
def getSmartNetControllerBodyDescription(headerFunction, headerFlag, body):
	if headerFunction not in constantsSmartNet.ControllerFunction:
		return ''
		
	function = constantsSmartNet.ControllerFunction[headerFunction]

	functionParserDict = {
		'I_AM_HERE'        : smartNetControllerIAmHereDescription,
		'GET_OUTPUT_VALUE' : smartNetControllerGetOutputValueBodyDescription,
		'JOURNAL'          : smartNetControllerJournalBodyDescription,
		'INIT_LOG_TRANSMIT': smartNetControllerInitLogTransmitDescription,
		'GET_LOG_PART'     : smartNetControllerGetLogPartDescription,
		'GET_RELAY_MAPPING': smartNetControllerGetRelayMappingDescription,
	}

	if function in functionParserDict:
		return functionParserDict[function](headerFlag, body)
	
	return ''

def hexArrayToString(array):
	hexString = ''.join(array)
	byte_array = bytearray.fromhex(hexString)
	return byte_array.decode().strip('\0')

def parseTitleParameterRead(value, headerFlag):
	pos = int(value[0], 16)
	if pos == 0:
		length = int(value[1], 16)
		crc16  = value[2]+value[3]
		
		if headerFlag == 1:
			parseTitleParameterRead.title  = []
			parseTitleParameterRead.length = length
			
		return f'len={length:>2} crc={crc16}'
		
	parseTitleParameterRead.title.append({
		'pos':pos,
		'value':value[1:]
		})
	
	hexStringPart = ''.join(value[1:])
	
	length = 0
	for t in parseTitleParameterRead.title:
		length += len(t['value'])
		if parseTitleParameterRead.length > 0 and length >= parseTitleParameterRead.length:
			text = [None] * parseTitleParameterRead.length
			for t in parseTitleParameterRead.title:
				i = 0
				for c in t['value']:
					text[t['pos'] - 1 + i] = c
					i += 1
					
			parseTitleParameterRead.title  = []
			parseTitleParameterRead.length = 0
			
			title = hexArrayToString(text)
			return f'{pos:>2}: {hexStringPart} = {title}'
	
	return f'{pos:>2}: {hexStringPart}'

parseTitleParameterRead.title  = []
parseTitleParameterRead.length = 0
	
def parseRemoteControlProgramGetParameterValue(parameter, headerFlag, value):
	if (parameter == 'OUTPUT_MAPPING' or
	    parameter == 'INPUT_MAPPING'):
		channelId = int(value[0], 16)
		if headerFlag == 0:
			return f'{channelId}'
			
		mappingStr = json.dumps(parseMappingValue(value[1:]))
		return f'{channelId}={mappingStr}'
	
	if parameter == 'TITLE':
		return parseTitleParameterRead(value, headerFlag)
		
	return ''
	
	

def smartNetRemoteControlGetParameterValueBodyDescription(headerFlag, body):
	bodyLen = len(body)

	programTypeId = int(body[0], 16)
	parameterId   = int(body[1], 16)
	
	if programTypeId not in constantsSmartNet.ProgramType:
		return ''
	
	programType = constantsSmartNet.ProgramType[programTypeId]
	
	if ((programType not in constantsSmartNet.ParameterDict) or
	 (parameterId not in constantsSmartNet.ParameterDict[programType])):
		parameter = parameterId
	else:
		parameter = constantsSmartNet.ParameterDict[programType][parameterId]
	
	parameterStr = f'{programType}.{parameter}:'
	
	if programType == 'PROGRAM':
		parameterStr += parseRemoteControlProgramGetParameterValue(parameter, headerFlag, body[2:])
	else:
		for i in range(2, bodyLen):
			parameterStr += ' ' + body[i]
		
	return parameterStr
	
def getSmartNetRemoteControlBodyDescription(headerFunction, headerFlag, body):
	if headerFunction not in constantsSmartNet.RemoteControlFunction:
		return ''
		
	function = constantsSmartNet.RemoteControlFunction[headerFunction]
	
	if function == 'GET_PARAMETER_VALUE' : return smartNetRemoteControlGetParameterValueBodyDescription(headerFlag, body)
	
	return ''
	
	
def getSmartNetBodyDescription(headerType, headerFunction, headerFlag, body):
	if headerType not in constantsSmartNet.ProgramType:
		return ''

	programType = constantsSmartNet.ProgramType[headerType]
	
	if programType == 'CONTROLLER'    : return getSmartNetControllerBodyDescription   (headerFunction, headerFlag, body)
	if programType == 'REMOTE_CONTROL': return getSmartNetRemoteControlBodyDescription(headerFunction, headerFlag, body)
	
	return ''
	
def parseSmartNetProtocolLine(line, t):
	parseSmartNetProtocolLine.i += 1
	
	if len(line) < 4:
		return
	
	try:
		pLine = parseCANUSBLineCommon(line)
	except:
		print('Line %d: %s fail' %(parseSmartNetProtocolLine.i, line))
		return
	
	if pLine['messageType'] != 'T':
		print('MessageType {}'.format(pLine['messageType']))
		return
	
	(	headerFlag,
		headerFunction,
		headerID,
		headerType
	) = parseSmartNetHeader(pLine['header'])
	
	if headerFlag == None:
		print('header: {}'.format(pLine['header']))
		return
	
	body      = pLine['body']
	timestamp = pLine['timestamp']
	delta     = pLine['deltaT']
	
	headerStr = ' '.join(pLine['header'])
	bodyStr   = ' '.join(body)
	
	
	
	headerDescription = getSmartNetHeaderDescription(headerID, headerType, headerFunction, headerFlag)
	bodyDescription   = getSmartNetBodyDescription  (headerType, headerFunction, headerFlag, body)
	
	t.add_row([	timestamp,
				delta,
				pLine['messageType'],
				headerStr,
				bodyStr,
				headerDescription,
				bodyDescription
			])
	
#init static var
parseSmartNetProtocolLine.i = 0

def parseSmartNetProtocol(content, outputFile):
	t = prepareSmartNetTable()

	for line in content:
		try:
			parseSmartNetProtocolLine(line, t)
		except:
			print(f'Bad Line {line}');
			exit(1)
	
	with open(outputFile, 'w') as Output: Output.write(t.get_string())
	