from prettytable import PrettyTable
import argparse

def splitAt(w,n):
    for i in range(0,len(w),n):
        yield w[i:i+n]

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Parse file name')
	parser.add_argument('File', metavar='MyFile', nargs='+',
                    help='file with CAN log')
					
	arg = parser.parse_args()
	FileToParse = arg.File[0]
	
	Input = open(FileToParse, 'r')
	content = Input.readlines()
	
	Output = open('Output.txt', 'w')
	
	
	ProgramType = {
	 0: 'CAN_PROGRAM_TYPE_UNDEFINED',
	 1: 'PROGRAM',
	 2: 'OUTDOOR_SENSOR',
	 3: 'CONSUMER',
	 4: 'CASCADE_MANAGER',
	 5: 'ROOM_DEVICE',
	 6: 'TEMPERATURE_SOURCE',
	 7: 'HEAT_ACCUMULATOR',
	 8: 'EXTENDED_CONTROLLER',
	 9: 'EXTENSION_CONTROLLER',
	10: 'MONITORING_DEVICE',
	11: 'CONTROLLER',
	12: 'CIRCUIT',
	13: 'SCHEDULE',
	14: 'HEATING_CIRCUIT',
	15: 'DIRECT_CIRCUIT',
	16: 'DHW',
	17: 'FLOW_THROUGH_DHW',
	18: 'TEMPERATURE_GENERATOR',
	19: 'POOL',
	20: 'THERMOSTAT',
	21: 'SNOWMELT',
	22: 'REMOTE_CONTROL',
	23: 'BOILER',
	24: 'CHILLER',
	25: 'SOLAR_COLLECTOR',
	26: 'VENTILATION',
	27: 'GENERIC_RELAY',
	28: 'ALARM',
	29: 'FILLING_LOOP',
    
	0x80 : 'DATALOGGER_MONITOR',
	0x81 : 'EVENT',
	0x82 : 'FWC_CASCADE',
	0x83 : 'DATALOGGER_NAMEDSENSORS',
	0x84 : 'HCC',
	0x85 : 'DL_CONFIGMENU_DATALOGGER',
	0x86 : 'DL_CONFIGMENU_CONTROLLER',
	0x87 : 'CLOCKSYNC'
	}

	t = PrettyTable(['T', 'dT', 'Header', 'Flag', 'Func', 'ID', 'Type', 'Body'])
	t.align = 'r'
	t.align['Body'] = 'l'
	
	oldTimestamp = 0
	
	for line in content:
		if line[0] == 't':
			headerSize = 2
		elif line[0] == 'T':
			headerSize = 4
		else: continue
			
		headerPos = 1
		headerLen = headerSize * 2
		
		header = line[headerPos : headerPos + headerLen]
		
		headerType = ProgramType[int(header[-2:],16)]
		headerID = int(header[-4:-2],16)
		headerFunction = int(header[-6:-4],16)
		#flag = 'RESP' if int(header[0]) else 'RQST'
		flag = header[0] #better to watch
		
		bodySizePos = headerPos + headerLen
		bodySizeLen = 1
		
		bodySize = line[bodySizePos : bodySizePos + bodySizeLen]
		
		bodyPos = bodySizePos + bodySizeLen
		bodyLen = int(bodySize) * 2
		
		body = line[bodyPos : bodyPos + bodyLen]
		tmp = " ".join(splitAt(body,2))
		body = tmp
		
		tmp = " ".join(splitAt(header,2))
		header = tmp
		
		timestamp = int(line[-5:-1], 16)
		
		delta = timestamp - oldTimestamp
		
		t.add_row([timestamp, delta, header, flag, headerFunction, headerID, headerType, body])

		oldTimestamp = timestamp
		
	Output.write(t.get_string())
	Input.close()
	Output.close()
	
	print 'Done'