import minimalmodbus
import serial
import os
import time
from time import sleep
from datetime import datetime
import pandas as pd
import csv
# import logging
newline = 0
counter = 0
simpandata = 0
COM = 'COM4'

while True :
    try :
        instrument = minimalmodbus.Instrument (COM, 70)
        instrument.serial.baudrate = 9600
        instrument.serial.bytesize = 8
        instrument.serial.parity = serial.PARITY_NONE
        instrument.serial.stopbits = 2
        instrument.serial.timeout = 1
        instrument.mode = minimalmodbus.MODE_RTU
        instrument.close_port_after_each_call = True
        data = instrument.read_register (0x03e8, 1, 0x04, signed = True)
        devicecondition = "ON"

    except Exception as exc:
        with open('errorread.csv', 'a') as errorlog:
            errorlog.write(str(exc) + ',' + '\n')
        errorlog.close()
        data = 0
        devicecondition = "OFF"

    separator = ','
    newtemperature = data
    try :
        with open('chiller.csv', 'a') as logging:
            logging.write(str(newline) + ',' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ',' + str(
                newtemperature) + ',' + '\n')
        logging.close()
        print(str(newline) + ',' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ',' + str(newtemperature))
    except :
        print("gabisa")

    time.sleep(60)
    temperature = devices = None

