

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

def getBodyLenFromString(bodySizeStr):
	return int(bodySizeStr, 16) * 2


def parseCANUSBLineCommon(line):
	messageType, line = cutFromLine(line, 1)
	header     , line = cutFromLine(line, getHeaderLen(messageType))
	bodySize   , line = cutFromLine(line, 1)
	body       , line = cutFromLine(line, getBodyLenFromString(bodySize))
	timestamp  , line = cutFromLine(line, 4)
	
	header = splitAt(header, 2)
	body   = splitAt(body  , 2)
	
	if len(timestamp) == 4:
		timestamp = int(timestamp, 16)
	else:
		timestamp = 0
		
	return {
		'messageType' : messageType,
		'header'      : header,
		'body'        : body,
		'timestamp'   : timestamp,
	}
	
