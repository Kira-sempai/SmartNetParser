

kseModule = {
    0x03: 'Boiler'   ,
    0x06: 'Operating', # Bedien
    0x09: 'Manager'  ,
    0x0A: 'Heating'  , # Heizmodul
    0x0C: 'Mixer'    , # Mischer
	0x0D: 'CoCo'     ,
}

kseParameter = {
	0x01   : {'format':'default'    , 'name':'ErrorCode'                          },
	0x09   : {'format':'default'    , 'name':'Time'                               },
	0x0A   : {'format':'default'    , 'name':'Date'                               },
	0x0C   : {'format':'temperature', 'name':'OutsideAirTemperature'              },
	0x0D   : {'format':'temperature', 'name':'HeatSourceTemperature'              },
	0x0E   : {'format':'temperature', 'name':'DHWTemperature'                     },
	0x0F   : {'format':'temperature', 'name':'HC_FlowTemperature'                 },
	0x8C   : {'format':'default'    , 'name':'CascadePower'                       },
	0xA051 : {'format':'default'    , 'name':'HeatSourceStage1'                   },
	0xA151 : {'format':'default'    , 'name':'HeatSourceStage2'                   },
	
	0x0489 : {'format':'default'    , 'name':'AdditionalRelay1Function'           },
	0x048A : {'format':'default'    , 'name':'AdditionalRelay2Function'           },
	0x048B : {'format':'default'    , 'name':'AdditionalRelay3Function'           },
	0x048C : {'format':'default'    , 'name':'AdditionalRelay4Function'           },

	0x36   : {'format':'temperature', 'name':'AdditionalRelayTemperature'         },

	0x04A9 : {'format':'temperature', 'name':'AdditionalRelay1Temperature'        },
	0x04AA : {'format':'temperature', 'name':'AdditionalRelay2Temperature'        },
	0x04AB : {'format':'temperature', 'name':'AdditionalRelay3Temperature'        },
	0x04AC : {'format':'temperature', 'name':'AdditionalRelay4Temperature'        },
	
	0x04C9 : {'format':'temperature', 'name':'AdditionalRelay1Hysteresis'         },
	0x04CA : {'format':'temperature', 'name':'AdditionalRelay2Hysteresis'         },
	0x04CB : {'format':'temperature', 'name':'AdditionalRelay3Hysteresis'         },
	0x04CC : {'format':'temperature', 'name':'AdditionalRelay4Hysteresis'         },
	
	0x0529 : {'format':'default'    , 'name':'AdditionalRelay1'                   },
	0x052A : {'format':'default'    , 'name':'AdditionalRelay2'                   },
	0x052B : {'format':'default'    , 'name':'AdditionalRelay3'                   },
	0x052C : {'format':'default'    , 'name':'AdditionalRelay4'                   },

	0x02   : {'format':'temperature', 'name':'RequiredHeatSourceTemperature'      },
	0x17   : {'format':'temperature', 'name':'DHWLowerTemperature'                },
	0x03   : {'format':'temperature', 'name':'DHWRequiredTemperature'             },
	0x13   : {'format':'temperature', 'name':'DHWRequiredTemperature1'            },
	0x0A06 : {'format':'temperature', 'name':'DHWRequiredTemperature2'            },
	0x013E : {'format':'temperature', 'name':'DHWRequiredTemperature3'            },
	0x5E   : {'format':'bit'        , 'name':'DHWHeatRequest'                     },
	0x0144 : {'format':'bit'        , 'name':'DHWSingleHeat'                      },
	0x0101 : {'format':'default'    , 'name':'DHWAntilegionella'                  },
	0x0182 : {'format':'default'    , 'name':'DHWCirculation'                     },
	
	0x52   : {'format':'bit'        , 'name':'HC_Pump'                            },
	0x53   : {'format':'bit'        , 'name':'DHWLoadingPump'                     },
	
	0x0103 : {'format':'default'    , 'name':'HC_WarmupOptimization'              },
	0x0109 : {'format':'default'    , 'name':'HC_RoomSensorAdaptation'            },
	0x010E : {'format':'default'    , 'name':'HC_HeatSlope'                       },
	0x010F : {'format':'default'    , 'name':'HC_RoomHeatingInfluence'            },
	0x0110 : {'format':'default'    , 'name':'HC_MaxHeatingForwarding'            },
	0x0111 : {'format':'temperature', 'name':'HC_HeatSlopeOffset'                 },
	0x0112 : {'format':'default'    , 'name':'HC_UnitOperatingMode'               },
	
	0x0115 : {'format':'default'    , 'name':'HC_AutomaticHeatSlopeAdaptation'    },
	0x0116 : {'format':'temperature', 'name':'HC_HeatingLimitTempDay'             },
	0x0117 : {'format':'temperature', 'name':'HC_HeatingLimitTempNight'           },
	
	0x04   : {'format':'temperature', 'name':'HC_RequiredFlowTemperature'         },
	0x11   : {'format':'temperature', 'name':'HC_RoomTemperature'                 },
	0x12   : {'format':'temperature', 'name':'HC_RequiredRoomTemperature'         },
	0x05   : {'format':'temperature', 'name':'HC_RequiredRoomTemperature1'        },
	0x06   : {'format':'temperature', 'name':'HC_RequiredRoomTemperature2'        },
	0x07   : {'format':'temperature', 'name':'HC_RequiredRoomTemperature3'        },	
	0x08   : {'format':'temperature', 'name':'HC_RequiredNighttimeRoomTemperature'},
	0x010C : {'format':'temperature', 'name':'HC_OutsideTemperatureDelay'         },
	
	
	0x018F : {'format':'bit'        , 'name':'HC_MixerOpen'                       },
	0x019D : {'format':'bit'        , 'name':'HC_MixerClose'                      },
	
	
	0x0187 : {'format':'default'    , 'name':'NoHWHeatGenerators'                 },
	
	0x0129 : {'format':'temperature', 'name':'HC_RequiredDayFlowTemperature'      },
	0x012A : {'format':'temperature', 'name':'HC_RequiredNightFlowTemperature'    },
	0x012B : {'format':'temperature', 'name':'HC_MinFlowTemperature'              },
	0x012E : {'format':'default'    , 'name':'HC_OptimizationOfReduction'         },
	0x013D : {'format':'temperature', 'name':'HC_RequiredAbsenceRoomTemperature'  },
	
	0x0141 : {'format':'default'    , 'name':'HC_Function'                        },
	0xFDC9 : {'format':'default'    , 'name':'HC_ReceiveCoercion'                 },
	
	0x20   : {'format':'default'    , 'name':'HeatSourceWarmupTemperature'        },
	0x21   : {'format':'default'    , 'name':'HeatSourceHysteresisTime'           },
	0x22   : {'format':'default'    , 'name':'HeatSourceHysteresis'               },
	0x25   : {'format':'default'    , 'name':'HeatSourceSecondStageBlockTime'     },
	0x26   : {'format':'default'    , 'name':'HeatSourceSecondStageHysteresis'    },
	0x2E   : {'format':'temperature', 'name':'HeatSourceMinimumTemperatureLimiter'},
	
	0x28   : {'format':'temperature', 'name':'HC_MaxFlowTemperature'              },
    0x0A00 : {'format':'temperature', 'name':'HC_FrostProtectionTemperature'      },
	
	0x029A : {'format':'temperature', 'name':'HeatSourceMaxTemperature'           },
	0x029B : {'format':'temperature', 'name':'HeatSourceMinTemperature'           },
	
	0x03E9 : {'format':'default'    , 'name':'BurnerBoiler1Stage1Power' },
	0x03EA : {'format':'default'    , 'name':'BurnerBoiler2Stage1Power' },
	0x03EB : {'format':'default'    , 'name':'BurnerBoiler3Stage1Power' },
	0x03EC : {'format':'default'    , 'name':'BurnerBoiler4Stage1Power' },
	0x03ED : {'format':'default'    , 'name':'BurnerBoiler5Stage1Power' },
	0x03EE : {'format':'default'    , 'name':'BurnerBoiler6Stage1Power' },
	0x03EF : {'format':'default'    , 'name':'BurnerBoiler7Stage1Power' },
	0x03F0 : {'format':'default'    , 'name':'BurnerBoiler8Stage1Power' },
	
	0x03F9 : {'format':'default'    , 'name':'BurnerBoiler1Stage2Power' },
	0x03FA : {'format':'default'    , 'name':'BurnerBoiler2Stage2Power' },
	0x03FB : {'format':'default'    , 'name':'BurnerBoiler3Stage2Power' },
	0x03FC : {'format':'default'    , 'name':'BurnerBoiler4Stage2Power' },
	0x03FD : {'format':'default'    , 'name':'BurnerBoiler5Stage2Power' },
	0x03FE : {'format':'default'    , 'name':'BurnerBoiler6Stage2Power' },
	0x03FF : {'format':'default'    , 'name':'BurnerBoiler7Stage2Power' },
	0x0400 : {'format':'default'    , 'name':'BurnerBoiler8Stage2Power' },
	
	0x0409 : {'format':'default'    , 'name':'Boiler1STStarts1'},
	0x040A : {'format':'default'    , 'name':'Boiler2STStarts1'},
	0x040B : {'format':'default'    , 'name':'Boiler3STStarts1'},
	0x040C : {'format':'default'    , 'name':'Boiler4STStarts1'},
	0x040D : {'format':'default'    , 'name':'Boiler5STStarts1'},
	0x040E : {'format':'default'    , 'name':'Boiler6STStarts1'},
	0x040F : {'format':'default'    , 'name':'Boiler7STStarts1'},
	0x0410 : {'format':'default'    , 'name':'Boiler8STStarts1'},
	
	0x0419 : {'format':'default'    , 'name':'Boiler1STStarts2'},
	0x041A : {'format':'default'    , 'name':'Boiler2STStarts2'},
	0x041B : {'format':'default'    , 'name':'Boiler3STStarts2'},
	0x041C : {'format':'default'    , 'name':'Boiler4STStarts2'},
	0x041D : {'format':'default'    , 'name':'Boiler5STStarts2'},
	0x041E : {'format':'default'    , 'name':'Boiler6STStarts2'},
	0x041F : {'format':'default'    , 'name':'Boiler7STStarts2'},
	0x0420 : {'format':'default'    , 'name':'Boiler8STStarts2'},
	
	0x0449 : {'format':'default'    , 'name':'Boiler1STWorkTime1'},
	0x044A : {'format':'default'    , 'name':'Boiler2STWorkTime1'},
	0x044B : {'format':'default'    , 'name':'Boiler3STWorkTime1'},
	0x044C : {'format':'default'    , 'name':'Boiler4STWorkTime1'},
	0x044D : {'format':'default'    , 'name':'Boiler5STWorkTime1'},
	0x044E : {'format':'default'    , 'name':'Boiler6STWorkTime1'},
	0x044F : {'format':'default'    , 'name':'Boiler7STWorkTime1'},
	0x0450 : {'format':'default'    , 'name':'Boiler8STWorkTime1'},
	
	0x0459 : {'format':'default'    , 'name':'Boiler1STWorkTimeOverflow1'},
	0x045A : {'format':'default'    , 'name':'Boiler2STWorkTimeOverflow1'},
	0x045B : {'format':'default'    , 'name':'Boiler3STWorkTimeOverflow1'},
	0x045C : {'format':'default'    , 'name':'Boiler4STWorkTimeOverflow1'},
	0x045D : {'format':'default'    , 'name':'Boiler5STWorkTimeOverflow1'},
	0x045E : {'format':'default'    , 'name':'Boiler6STWorkTimeOverflow1'},
	0x045F : {'format':'default'    , 'name':'Boiler7STWorkTimeOverflow1'},
	0x0460 : {'format':'default'    , 'name':'Boiler8STWorkTimeOverflow1'},
	
	0x0469 : {'format':'default'    , 'name':'Boiler1STWorkTime2'},
	0x046A : {'format':'default'    , 'name':'Boiler2STWorkTime2'},
	0x046B : {'format':'default'    , 'name':'Boiler3STWorkTime2'},
	0x046C : {'format':'default'    , 'name':'Boiler4STWorkTime2'},
	0x046D : {'format':'default'    , 'name':'Boiler5STWorkTime2'},
	0x046E : {'format':'default'    , 'name':'Boiler6STWorkTime2'},
	0x046F : {'format':'default'    , 'name':'Boiler7STWorkTime2'},
	0x0470 : {'format':'default'    , 'name':'Boiler8STWorkTime2'},
	
	0x0479 : {'format':'default'    , 'name':'Boiler1STWorkTimeOverflow2'},
	0x047A : {'format':'default'    , 'name':'Boiler2STWorkTimeOverflow2'},
	0x047B : {'format':'default'    , 'name':'Boiler3STWorkTimeOverflow2'},
	0x047C : {'format':'default'    , 'name':'Boiler4STWorkTimeOverflow2'},
	0x047D : {'format':'default'    , 'name':'Boiler5STWorkTimeOverflow2'},
	0x047E : {'format':'default'    , 'name':'Boiler6STWorkTimeOverflow2'},
	0x047F : {'format':'default'    , 'name':'Boiler7STWorkTimeOverflow2'},
	0x0480 : {'format':'default'    , 'name':'Boiler8STWorkTimeOverflow2'},
	
	0x0549 : {'format':'temperature', 'name':'TemperatureBoiler1'},
	0x054A : {'format':'temperature', 'name':'TemperatureBoiler2'},
	0x054B : {'format':'temperature', 'name':'TemperatureBoiler3'},
	0x054C : {'format':'temperature', 'name':'TemperatureBoiler4'},
	0x054D : {'format':'temperature', 'name':'TemperatureBoiler5'},
	0x054E : {'format':'temperature', 'name':'TemperatureBoiler6'},
	0x054F : {'format':'temperature', 'name':'TemperatureBoiler7'},
	0x0550 : {'format':'temperature', 'name':'TemperatureBoiler8'},
	
	0x0559 : {'format':'default'    , 'name':'KModulation1'},
	0x055A : {'format':'default'    , 'name':'KModulation2'},
	0x055B : {'format':'default'    , 'name':'KModulation3'},
	0x055C : {'format':'default'    , 'name':'KModulation4'},
	0x055D : {'format':'default'    , 'name':'KModulation5'},
	0x055E : {'format':'default'    , 'name':'KModulation6'},
	0x055F : {'format':'default'    , 'name':'KModulation7'},
	0x0560 : {'format':'default'    , 'name':'KModulation8'},
	
	0x09E6 : {'format':'default'    , 'name':'HeatSourceCoolingFunction'           },
	0x09E7 : {'format':'default'    , 'name':'HeatSourceCoolingFunctionTemperature'},
	
	0x09FD : {'format':'default'    , 'name':'CascadingHeatSourceMaximumTemperature'},
	0x09FE : {'format':'default'    , 'name':'HeatSourceStagesRotationPeriod'       },
	
	0xE042 : {'format':'default'    , 'name':'HeatSourceUnderheatStart' },
	0xE044 : {'format':'default'    , 'name':'DHWUnderheatStart'        },
	0xE046 : {'format':'default'    , 'name':'HCFlowUnderheatStart'     },
	0xE048 : {'format':'default'    , 'name':'HCRoomUnderheatStart'     },
	
	0xE050 : {'format':'default'    , 'name':'BurnerBoiler1Stage1'},
	0xE051 : {'format':'default'    , 'name':'BurnerBoiler2Stage1'},
	0xE052 : {'format':'default'    , 'name':'BurnerBoiler3Stage1'},
	0xE053 : {'format':'default'    , 'name':'BurnerBoiler4Stage1'},
	0xE054 : {'format':'default'    , 'name':'BurnerBoiler5Stage1'},
	0xE055 : {'format':'default'    , 'name':'BurnerBoiler6Stage1'},
	0xE056 : {'format':'default'    , 'name':'BurnerBoiler7Stage1'},
	0xE057 : {'format':'default'    , 'name':'BurnerBoiler8Stage1'},
	
	0xE058 : {'format':'default'    , 'name':'BurnerBoiler1Stage2'},
	0xE059 : {'format':'default'    , 'name':'BurnerBoiler2Stage2'},
	0xE05A : {'format':'default'    , 'name':'BurnerBoiler3Stage2'},
	0xE05B : {'format':'default'    , 'name':'BurnerBoiler4Stage2'},
	0xE05C : {'format':'default'    , 'name':'BurnerBoiler5Stage2'},
	0xE05D : {'format':'default'    , 'name':'BurnerBoiler6Stage2'},
	0xE05E : {'format':'default'    , 'name':'BurnerBoiler7Stage2'},
	0xE05F : {'format':'default'    , 'name':'BurnerBoiler8Stage2'},
	
	
	0xFDC1 : {'format':'default'    , 'name':'HC_WorkMode'},
	0xFDC8 : {'format':'default'    , 'name':'HC_PumpOperatingMode'},
	
	0xFDED : {'format':'default'    , 'name':'CascadeSequenceChangeMode'},
}

