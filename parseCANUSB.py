from prettytable import PrettyTable
import argparse
import constants
import datetime
import os
from test.test_funcattrs import FunctionDictsTest
from compiler.ast import Const
from email.base64mime import body_decode

def splitAt(w,n):
	list = []
	for i in range(0,len(w),n):
		list.append(w[i:i+n])
	return list

def cutFromLine(line, n):
	if not n: return '', line
	
	if len(line) < n: return '', line
	
	return line[:n], line[n:]

def getHeaderLen(messageType):
	if messageType.islower():
		return 3
	
	return 8

def prepareSmartNetTable():
	t = PrettyTable([	'T',
						'dT',
						'MT',
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
	t.align['Parsed body'] = 'l'
	return t

def parseSmartNetCANUSBLine(line):
	messageType, line = cutFromLine(line, 1)
	headerLen = getHeaderLen(messageType)
	if headerLen != 8: return messageType, None, None, None
	
	header, line = cutFromLine(line, headerLen)
	header = splitAt(header, 2)
	
	bodySize, line = cutFromLine(line, 1)
	bodySize = int(bodySize, 16)
	body, line = cutFromLine(line, bodySize * 2)
	body = splitAt(body, 2)
	timestamp, line = cutFromLine(line, 4)
	
	if len(timestamp) == 0:
		timestamp = '0000'
	
	return messageType, header, body, int(timestamp, 16)

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
		
		if (self.type in constants.ProgramType) and (constants.ProgramType[self.type] in constants.Function):
			self.functionDict = constants.Function[constants.ProgramType[self.type]]
		else:
			self.functionDict = None	
		
	
	def getProgramTypeName(self):
		if self.type in constants.ProgramType:
			return constants.ProgramType[self.type]
		
		return 'UNK_Type'
		
	def getFunctionName(self, functionId):
		if self.functionDict and (functionId in self.functionDict):
			return self.functionDict[functionId]
		
		return 'UNK_Func'


def getSmartNetHeaderDescription(id, programTypeId, functionId, flag):
	prg = Program(id, programTypeId)
	
	programTypeName = prg.getProgramTypeName()
	functionName    = prg.getFunctionName(functionId)
	flagName        = constants.smartNetHeaderFlag[flag]
	
	return '{}({:3})->{} {:8}'.format(programTypeName, id, functionName, flagName)


def smartNetControllerGetOutputValueBodyDescription(flag, body):
	host = int(body[0], 16)
	
	channelIdAndType = int(body[1], 16)
	
	channelId = channelIdAndType & 0x1F
	channelType = channelIdAndType >> 5
	
	
	typeDict = {
		0: 'CHANNEL_SENSOR_LOCAL',
		1: 'CHANNEL_RELAY_LOCAL',
		2: 'CHANNEL_SENSOR',
		3: 'CHANNEL_RELAY',
		4: 'CHANNEL_INPUT',
		5: 'CHANNEL_OUTPUT',
#		6: 'CHANNEL_RESERVED',
		7: 'CHANNEL_UNDEFINED',
	}
	
	channelTypeName = typeDict[channelType]
	
	if flag == 0:
		return ''
	
	if channelType == 5:
		value = int(body[2], 16)
	elif channelType == 2:
		value = int('{}{}'.format(body[2], body[3]), 16)/10.0
	else:
		value = ''
	
	return 'host={:2} channelId={:2} type={:14} value={:5}'.format(host, channelId, channelTypeName, value)

def smartNetControllerJournalBodyDescription(flag, body):
	if (flag == 0):
		return ''
	
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
	
	if operation == 0:
		crc16 = int('{}{}'.format(body[2], body[1]), 16)
		timestamp = int('{}{}{}{}'.format(body[6], body[5], body[4], body[3]), 16)
		messageDateTime = datetime.datetime.utcfromtimestamp(timestamp)
	else:
		severity = int(body[1], 16)
		crc16 = int('{}{}'.format(body[3], body[2]), 16)
		timestamp = int('{}{}{}{}'.format(body[7], body[6], body[5], body[4]), 16)
		messageDateTime = datetime.datetime.utcfromtimestamp(timestamp)
	
	return ''

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
	
	if control.has_key(chunkControlInt):
		chunkControlStr = control[chunkControlInt]
	else:
		chunkControlStr = str(chunkControlInt)
	
	bodyStartStr = (str(chunkId) + '.' + chunkControlStr)
	
	if constants.smartNetHeaderFlag[flag] == 'Request':
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
	if not constants.ControllerFunction.has_key(headerFunction):
		return ''
		
	function = constants.ControllerFunction[headerFunction]

	if function == 'GET_OUTPUT_VALUE' : return smartNetControllerGetOutputValueBodyDescription(headerFlag, body)
	if function == 'JOURNAL'          : return smartNetControllerJournalBodyDescription(headerFlag, body)
	if function == 'INIT_LOG_TRANSMIT': return smartNetControllerInitLogTransmitDescription(headerFlag, body)
	if function == 'GET_LOG_PART'     : return smartNetControllerGetLogPartDescription(headerFlag, body)
	
	return ''
	
	
def smartNetRemoteControlGetParameterValueBodyDescription(headerFlag, body):
	bodyLen = len(body)

	programTypeId = int('{}'.format(body[0]), 16)
	parameterId   = int('{}'.format(body[1]), 16)
	
	if not constants.ProgramType.has_key(programTypeId):
		return ''
	
	programType = constants.ProgramType[programTypeId]
	
	if programType == 'ROOM_DEVICE': 
		parameter = constants.RoomDeviceParameter[parameterId]
		parameterStr = '{}.{}:'.format(programType, parameter)
	else:
		parameterStr = '{}.{}:'.format(programType, parameterId)
	
	for i in range(2, bodyLen):
		parameterStr + ' {}'.format(body[i])
		
	return parameterStr
	
def getSmartNetRemoteControlBodyDescription(headerFunction, headerFlag, body):
	if not constants.RemoteControlFunction.has_key(headerFunction):
		return ''
		
	function = constants.RemoteControlFunction[headerFunction]
	
	if function == 'GET_PARAMETER_VALUE' : return smartNetRemoteControlGetParameterValueBodyDescription(headerFlag, body)
	
	return ''
	
	
def getSmartNetBodyDescription(headerType, headerFunction, headerFlag, body):
	if not constants.ProgramType.has_key(headerType):
		return ''

	programType = constants.ProgramType[headerType]
	
	if programType == 'CONTROLLER'    : return getSmartNetControllerBodyDescription   (headerFunction, headerFlag, body)
	if programType == 'REMOTE_CONTROL': return getSmartNetRemoteControlBodyDescription(headerFunction, headerFlag, body)
	
	return ''
	
	
def parseSmartNetProtocol(content, outputFile):
	t = prepareSmartNetTable()

	oldTimestamp = 0
	for line in content:
		messageType, header, body, timestamp = parseSmartNetCANUSBLine(line)
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
		
		headerDescription = getSmartNetHeaderDescription(headerID, headerType, headerFunction, headerFlag)
		bodyDescription   = getSmartNetBodyDescription(headerType, headerFunction, headerFlag, body)
		
		t.add_row([	timestamp,
					delta,
					messageType,
					headerStr,
					headerFlag,
					headerFunction,
					headerID,
					headerType,
					bodyStr,
					headerDescription,
					bodyDescription
				])
	
	with open(outputFile, 'w') as Output: Output.write(t.get_string())
	
	
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
	
def parseKseCANUSBLine(line):
	messageType, line = cutFromLine(line, 1)
	headerLen = getHeaderLen(messageType)
	
	if headerLen != 3: return messageType, None, None, None
	
	header, line = cutFromLine(line, headerLen)
	
	bodySize, line = cutFromLine(line, 1)
	bodySize = int(bodySize, 16)
	body, line = cutFromLine(line, bodySize * 2)
	body = splitAt(body, 2)
	timestamp, line = cutFromLine(line, 4)
	
	return messageType, header, body, int(timestamp, 16)

	
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
	
	
def parseKseProtocol(content, outputFile):
	t = prepareKseTable()
	oldTimestamp = 0
	for line in content:
		messageType, header, body, timestamp = parseKseCANUSBLine(line)
		if not header: continue
		
		module, busId = parseKseHeader(header)
		
		bodyStr   = ' '.join(body)
		
		delta = timestamp - oldTimestamp
		oldTimestamp = timestamp
		
		parsedHeader = getKseModuleName(module)
		parsedBody   = getKseBodyDescription(body)
		
		t.add_row([	timestamp,
					delta,
					messageType,
					header,
					format(module, '#04x'),
					busId,
					bodyStr,
					parsedHeader,
					parsedBody
				])
	
	with open(outputFile, 'w') as Output: Output.write(t.get_string())


if __name__ == "__main__":
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
	
	
	print 'Done'
	
	