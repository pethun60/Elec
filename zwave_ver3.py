#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave wrapper
.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>
License : GPL(v3)
**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.
"""
import sys, os
import time
import libopenzwave
from datetime import datetime
from libopenzwave import PyManager
import paho.mqtt.client as mqtt
import logging
import opcua_client_lib as opcclient


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


# define file handler and set formatter
file_handler = logging.FileHandler('logfile.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)



device="/dev/ttyACM0"
log="Info"
sniff=60.0
dateTimeObject=datetime.now()
testbool=False

for arg in sys.argv:
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    elif arg.startswith("--sniff"):
        temp,sniff = arg.split("=")
        sniff = float(sniff)
    if arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")
        print("  --sniff=0 : sniff for zwave messages a number of seconds")
        exit(0)

options = libopenzwave.PyOptions(config_path="/home/peter/venv3/lib/python3.6/site-packages/python_openzwave/ozw_config/config", \
user_path=".", cmd_line="--logging false")

# Specify the open-zwave config path here
options.lock()
manager = libopenzwave.PyManager()
manager.create()

def temp_save(valuetype, meas_value, unit_type, time_obj, file_name):
    print(valuetype)
    print(meas_value)
    print(unit_type)
    logger.debug('temp_save value saved' + valuetype + str(meas_value))
    f= open(file_name,"a+")
    f.write(str(time_obj) + "\n")
    f.write("type " +  valuetype +"\n")
    f.write("value " + str(meas_value) + "\n")
    f.close()

def mqtt_save(valuetype, mqtt_value):

    def on_connect(client, userdata, flags, rc):
        if rc==0:
            client.connected_flag=True #set flag
            print("connected OK")
            logger.debug('connected OK to mqtt broker')
        else:
            print("Bad connection Returned code=",rc)
            logger.debug('Failed to connect to mqtt broker')

    input_topic="/temperatur/tobo/"+valuetype
    input_message=str(round(mqtt_value,1))
    input_host="thunholm.homelinux.com"
    user="remoteuser"
    password="Leokatt60"
    mqtt.Client.connected_flag=False # create connected_flag


    # This is the Publisher

    client = mqtt.Client()
    client.on_connect=on_connect
    client.username_pw_set(user, password=password)
    client.loop_start()
    print('connecting to broker' + input_host)
    logger.debug('connecting to broker' + input_host)
    client.connect(input_host,1883,60)
    while not client.connected_flag: #wait in loop
        print("In wait mqtt loop")
        time.sleep(1)
    print("mqtt connected or failed")
    client.loop_stop()
    client.publish(input_topic, input_message);
    client.disconnect();
    print("mqtt value" + str(mqtt_value))
    print(input_topic)
    logger.debug('mqtt_save value saved' + valuetype + str(mqtt_value))
    f= open("temp_RH.txt","a+")
    f.write("mqtt value" + str(round(mqtt_value,1)) + "\n")
    f.write(input_topic +"\n")
    f.close()

# callback order: (notificationtype, homeid, nodeid, ValueID, groupidx, event)
def callback(args):
    print('\n-------------------------------------------------')
    print('\n[{}]:\n'.format(args['notificationType']))
    print('\n[{}]:\n'.format(args))
    dateTimeObject=datetime.now()
    print("loop1")
    print(dateTimeObject)
    logger.debug('loop1 {}'.format(args['notificationType']))
    if args:
        print('homeId: 0x{0:08x}'.format(args['homeId']))
        print('nodeId: {}'.format(args['nodeId']))
        print("loop2")
        logger.debug('loop2 {}'.format(args['nodeId']))
        if 'valueId' in args:
            print("loop3")
            v = args['valueId']
            logger.debug('loop3 value id {}'.format(v['id']))
            print('valueID: {}'.format(v['id']))
            #if 'groupIndex' in v and v['groupIndex'] != 0xff: print('GroupIndex: {}'.format(v['groupIndex']))
            #if 'event' in v and v['event'] != 0xff: print('Event: {}'.format(v['event']))
            #if 'value' in v: print('Value: {}'..format(str(v['value']))format(str(v['value'])))
            if 'label' in v: print('Label: {}'.format(v['label']))
            #if 'units' in v: print('Units: {}'.format(v['units']))
            #if 'readOnly' in v: print('ReadOnly: {}'.format(v['readOnly']))
            dateTimeObject=datetime.now()
            print(dateTimeObject)
            #print(v['event'])
            #print(v['label'])

            valuetype=v['label']
            measured_value=v['value']
            unit_value=v['units']
            nodenumber=v['nodeId']
            logger.debug('loop3 values ' + valuetype + ' ' + str(measured_value))
            print(valuetype)
            print(measured_value)
            print(unit_value)
            print('nodnummer:')
            print(nodenumber)
            if (valuetype=="Temperature" or valuetype=="Relative Humidity" or valuetype=="Battery Level" or testbool) and nodenumber==3:
                print(' true value node 3!!')
                temp_save(valuetype, measured_value, unit_value, dateTimeObject,"temp_RH.txt")
                mqtt_save(valuetype, measured_value)
                opcclient.write_values(measured_value)
            if (valuetype=="Temperature" or valuetype=="Luminance" or valuetype =="Burglar" or valuetype=="Sensor") and nodenumber==4:
                print(' true value node 4!!')
                if valuetype=="Temperature":
                   valuetype='Motiontemperature'
                temp_save(valuetype, measured_value, unit_value, dateTimeObject, "temp_luminance.txt")
                mqtt_save(valuetype, measured_value)
                opcclient.write_values(measured_value)

    print('end ---- callback -------------------------------------------------\n')

print("Add watcher")
manager.addWatcher(callback)
print("Add device")
manager.addDriver(device)
print("Sniff network during {} seconds".format(sniff))
#time.sleep(sniff)
try:
    while True:
        time.sleep (0.1)
except KeyboardInterrupt:
    print("Remove watcher")
manager.removeWatcher(callback)
print("Remove device")
manager.removeDriver(device)
