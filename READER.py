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

def checkingsch():
    with open('schedule.csv', 'r') as scheduler:
        next(scheduler)
        timedead = []
        timelife = []
        addrssch = []
        for row in csv.reader(scheduler, delimiter=','):
            timedead.append(row[1])
            timelife.append(row[2])
            addrssch.append(row[3])
    scheduler.close()
    checkline = 0
    for time in timedead :
        try:
            timecheck = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            if datetime.now() == timecheck:
                try :
                    instrument40 = minimalmodbus.Instrument(COM, int(addrssch[checkline]))
                    instrument40.serial.baudrate = 9600
                    instrument40.serial.bytesize = 8
                    instrument40.serial.parity = serial.PARITY_NONE
                    instrument40.serial.stopbits = 2
                    instrument40.serial.timeout = 1
                    instrument40.mode = minimalmodbus.MODE_RTU
                    instrument40.write_register(0x0000, 0, 0x06)
                    instrument40.close_port_after_each_call = True
                except:
                    continue
        except:
            continue
        checkline = checkline+1
    checkline = None

    for time in timelife :
        try:
            timelifecheck = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            if datetime.now() == timelifecheck:
                checklinelife = timedead.index(timelifecheck)
                try :
                    xxxx = inputpres20.get()
                    try:
                        instrument40 = minimalmodbus.Instrument(COM, int(addrssch[checklinelife]))
                        instrument40.serial.baudrate = 9600
                        instrument40.serial.bytesize = 8
                        instrument40.serial.parity = serial.PARITY_NONE
                        instrument40.serial.stopbits = 2
                        instrument40.serial.timeout = 1
                        instrument40.mode = minimalmodbus.MODE_RTU
                        instrument40.write_register(0x0039, float(xxxx), 0x06)
                        instrument40.close_port_after_each_call = True
                    except:
                        xxxx = 0
                except :
                    print("0")
        except :
            print("oops")
    timedead = timelife = addrssch = None

def checkrequest():
    nomor = []
    requestdata = []

    with open('request.csv', 'r') as csvfile:
        for row in csv.reader(csvfile, delimiter=','):
            nomor.append(int(row[0]))
        nomorsekarang = len(nomor)
    csvfile.close()

    with open('request.csv', 'r') as csvfile:
        for x, line in enumerate(csv.reader(csvfile)):
            if x == nomorsekarang - 1:
                for y in line:
                    requestdata.append(y)
    csvfile.close()
    print(requestdata)
    try:
        instrument = minimalmodbus.Instrument(COM, int(requestdata[0]))
        instrument.serial.baudrate = 9600
        instrument.serial.bytesize = 8
        instrument.serial.parity = serial.PARITY_NONE
        instrument.serial.stopbits = 1
        instrument.serial.timeout = 1
        instrument.mode = minimalmodbus.MODE_RTU
        instrument.close_port_after_each_call = True
        data = instrument.read_register(0x03eb, 1, 0x04, signed=True)
        if data != requestdata[1] :
            instrument.write_register(0x0039, float (requestdata[1]) / 100000, 0x06)
    except:
        print("cannot change data")

def read () :
    global simpandata
    temperature = []
    with open('devicelist.csv', 'r') as deviceslisted:
        devices = []
        devicereader = csv.reader(deviceslisted, delimiter=',')
        next(devicereader)
        for cols in devicereader:
            devices.append(cols[1])
        print(devices)
    deviceslisted.close()

    for device in devices :
        try :
            instrument = minimalmodbus.Instrument (COM, int(device))
            instrument.serial.baudrate = 9600
            instrument.serial.bytesize = 8
            instrument.serial.parity = serial.PARITY_NONE
            instrument.serial.stopbits = 1
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

        temperature.append(float(data))
        temperature.append(str(devicecondition))

    separator = ','
    newtemperature = separator.join ([str(x) for x in temperature])
    print(newtemperature)

    if simpandata == 50:
        simpandata = 0
        try :
            with open('logging.csv', 'a') as logging:
                increasenewline()
                logging.write(str(newline) + ',' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ',' + str(
                    newtemperature) + ',' + '\n')
            logging.close()
        except :
            pass

    if simpandata < 50:
        simpandata = simpandata + 1
        print("simpandata", simpandata)

    try :
        with open('realtimedata.csv', 'w') as logrealtime:
            logrealtime.write(str(0) + ',' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ',' + str(newtemperature) + ',')
        logrealtime.close()

    except :
        pass

    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    temperature = devices = None

def increasenewline () :
    global newline
    with open('logging.csv', 'r') as logging :
        number = []
        readerfornumber = csv.reader(logging, delimiter=',')
        next(readerfornumber)
        for row in readerfornumber :
            number.append(int(row[0]))
        newline = len(number)
    newline = newline
    number = None
    logging.close()
    return newline

def counterrun () :
    global counter
    counter = counter + 1
    return counter

while True :
    global counter
    counterrun ()
    if counter == 6 :
        read ()
        checkrequest()
        counter = 0
    time.sleep (1)