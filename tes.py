import minimalmodbus
import serial

for device in range (1,44):
    instrument = minimalmodbus.Instrument('COM4', device)
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 1
    instrument.mode = minimalmodbus.MODE_RTU
    instrument.close_port_after_each_call = True
    data = instrument.read_register(0x03e8, 1, 0x04, signed=True)
    print(device, data)