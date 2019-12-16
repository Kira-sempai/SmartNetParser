
CANHeaderIDE = {
	't': 'STANDARD',
	'T': 'EXTENDED',
}

smartNetHeaderFlag = {
	0: 'Request',
	1: 'Response',
}

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
	0x87 : 'CLOCKSYNC',
	0x88 : 'REMOTERELAY',
	0x89 : 'HOLIDAYRETURNDATE',
	0x8A : 'DAYSCHEDULE',
	0x8B : 'AVAILABLERESOURCES',
	0x8C : 'PARAMETERSYNC',
	0x8D : 'RESOURCEDATA1WIRE',
	0x8E : 'FILETRANSFER',
	0x8F : 'PARAMETERSYNCCONFIG',
	0x90 : 'ROOMSYNC',
	0x91 : 'PANIC',
	0x92 : 'VHCDATA_UPDATE',
	
	0xC0 : 'CHARLIE',
}



ProgramFunction = {
	 1: 'IS_ID_OCCUPIED',
	 2: 'IS_TYPE_SUPPORTED',
	 3: 'GET_PROGRAM_TYPE',
	 4: 'GET_PROGRAM_NAME',
	 5: 'GET_PROGRAM_TYPES',
	 6: 'GET_SMARTNET_PROTOCOL_VERSION',
	 7: 'I_AM_PROGRAM',
	 8: 'IS_COLLISION',
	 9: 'MY_ID_CHANGED',
}



ControllerFunction = {
	 0: 'HAS_ANYBODY_HERE',
	 1: 'I_AM_HERE',
	 2: 'GET_CONTROLLER',
	 3: 'GET_ACTIVE_PROGRAMS_LIST',
	 4: 'ADD_NEW_PROGRAM',
	 5: 'REMOVE_PROGRAM',
	 6: 'GET_SYSTEM_DATE_TIME',
	 7: 'SET_SYSTEM_DATE_TIME',
	 8: 'GET_CONTROLLER_TYPE',
	 9: 'GET_PROGRAM_VERSION',
	10: 'GET_CHANNEL_NUMBER',
	11: 'GET_OUTPUT_TYPE',
	12: 'GET_INPUT_TYPE',
	13: 'GET_CHANNEL_BINDING',
	14: 'GET_INPUT_VALUE',
	15: 'SET_OUTPUT_VALUE',
	16: 'HAS_ERROR',
	17: 'GET_CONTROLLER_MASKS',
	18: 'GET_CHANNELS_INFO',
	19: 'GET_OUTPUT_VALUE',
	20: 'TIME_MASTER_IS_ACTIVE',

	21 : 'JOURNAL',

	22 : 'GET_VARIABLE',
	23 : 'SET_VARIABLE',

	24 : 'GET_RELAY_MAPPING',
	25 : 'SET_RELAY_MAPPING',

	26 : 'RESET_TO_DEFAULTS',
	27 : 'RESET_PROGRAMS',
	28 : 'MARK_JOURNAL_MESSAGES_AS_READ',
	
	
	40 : 'I_AM_RESETED',
	41 : 'DATALOGGER_TEST',
	42 : 'GET_FW_VERSION',
	43 : 'INSTALL_FW_UPDATE',
	44 : 'SYSTEM_SELFTEST',
	45 : 'GET_DEVICE_INFO',
	
	
	80 : 'INIT_LOG_TRANSMIT',
	81 : 'GET_LOG_PART',
	
}

RemoteControlFunction = {
	 1: 'GET_PARAMETER_VALUE',
	 2: 'SET_PARAMETER_VALUE',
	 3: 'GET_PARAMETER_NAME',
	 4: 'GET_PARAMETER_DESCRIPTION',
	 5: 'GET_PARAMETER_MINIMUM_VALUE',
	 6: 'GET_PARAMETER_MAXIMUM_VALUE',
	 7: 'GET_PARAMETER_DEFAULT_VALUE',
	 8: 'GET_PARAMETER_UNIT',
}

TemperatureSourceFunction = {
	0: 'REQUEST_TEMPERATURE',
	1: 'GET_TEMPERATURE',
	2: 'GET_PROPERTIES',
	3: 'REQUEST_POWER',
	4: 'GET_CURRENT_POWER',
	5: 'GET_WORK_TIME',
}

ConsumerFunction = {
	1: 'GIVE_WAY',
	2: 'PROCEED',
	3: 'SET_COOLING',
	4: 'SET_WARM_UP',
	5: 'GET_REQUESTED_TEMPERATURE',
}

HccFunction = {
	0x01: 'STATE_1',
	0x03: 'STATE_3',
	0x0F: 'MAPPING',
}

CircuitFunction = {
	1: 'RECEIVE_ROOM_STATUS',
}

ParameterSyncConfigFunction = {
	0: 'epsc_connect',            # data[0]: source, data[1]:destination
	1: 'epsc_factoryReset',         # reset all to defaults
	2: 'epsc_roomCount',            # tells other CALEONs number of rooms
	3: 'epsc_roomSyncDone',         # there are at least as many rooms as CALEONs present
	4: 'espc_setupWizard',          # setup wizard synchronization between CALEONs
	5: 'epsc_roomSyncStop',         # stop room sync
}


Function = {
	'PROGRAM'            : ProgramFunction,
	'CONSUMER'           : ConsumerFunction,
	'TEMPERATURE_SOURCE' : TemperatureSourceFunction,
	'CONTROLLER'         : ControllerFunction,
	'REMOTE_CONTROL'     : RemoteControlFunction,
	'HCC'                : HccFunction,
	'CIRCUIT'            : CircuitFunction,
	
	'PARAMETERSYNCCONFIG': ParameterSyncConfigFunction,
}

