#!/usr/bin/env python3
import serial

serial_port = serial.Serial(
    "/dev/ttyUSB0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=30,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False,
)
# serial_port.open()
while True:
    elec_data=serial_port.readline()
    print(elec_data)


# do something


serial_port.close()
