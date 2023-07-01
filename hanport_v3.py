#!/usr/bin/env python3
import serial
import paho.mqtt.client as mqtt
import logging
import time

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


# define file handler and set formatter
file_handler = logging.FileHandler('logfile.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)


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
    input_message=mqtt_value
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
    logger.debug('mqtt_save value saved' + valuetype + mqtt_value)
    f= open("temp_RH.txt","a+")
    f.write("mqtt value" + mqtt_value + "\n")
    f.write(input_topic +"\n")
    f.close()



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
read_lines=30
# serial_port.open()
while True:
    for i in range(read_lines):
        elec_data=serial_port.readline()
        #print (elec_data)
        #print(elec_data, 'length is', len(elec_data))
        #read_value = elec_data[10:24]
        #print (read_value)
        pos_start=elec_data.find('('.encode())+1
        pos_end=elec_data.find('*'.encode())
        pos_type=elec_data.find(')'.encode())
        if i==2:
           #print("rad 2")
           read_date = elec_data[10:22]
           datevalue=read_date.decode("utf-8")
           print ('date', datevalue)
        if i==3:
           print("startpos", pos_start)
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           active_energy_out=read_date.decode("utf-8")
           print ('active energiuttag  mätare',active_energy_out,valuetype)
        if i==4:
           #print("rad 4")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           active_energy_in=read_date.decode("utf-8")
           print ('active energi inmatning mätare', active_energy_in,valuetype)
        if i==5:
           #print("rad 5")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           reactive_energy_out=read_date.decode("utf-8")
           print ('reactive energi uttag', reactive_energy_out,valuetype)
        if i==6:
           #print("rad 6")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           reactive_energi_in=read_date.decode("utf-8")
           print ('reactive energi inmatning', reactive_energi_in,valuetype )
        if i==7:
           #print("rad 7aktiv")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           active_energy_out_curr=read_date.decode("utf-8")
           print ('aktiv effekt uttag', active_energy_out_curr,valuetype)
        if i==8:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           active_energy_in_curr=read_date.decode("utf-8")
           print ('aktiv effekt inmatning', active_energy_in_curr,valuetype)
        if i==9:
           #print("rad 7aktiv")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           reactive_energy_out_curr=read_date.decode("utf-8")
           print ('reaktiv effekt uttag', reactive_energy_out_curr,valuetype)
        if i==10:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           reactive_energy_in_curr=read_date.decode("utf-8")
           print ('reaktiv effekt inmatning', reactive_energy_in_curr,valuetype)
        if i==11:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1active_energy_out=read_date.decode("utf-8")
           print ('L1 Aktiv Effekt uttag', L1active_energy_out,valuetype)
        if i==12:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1active_energy_in=read_date.decode("utf-8")
           print ('L1 Aktive Effekt in', L1active_energy_in,valuetype)
        if i==13:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2active_energy_out=read_date.decode("utf-8")
           print ('L2 Aktiv Effekt uttag', L2active_energy_out,valuetype)
        if i==14:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2active_energy_in=read_date.decode("utf-8")
           print ('L2 Aktive Effekt in', L2active_energy_in,valuetype)
        if i==15:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3active_energy_out=read_date.decode("utf-8")
           print ('L3 Aktiv Effekt uttag', L3active_energy_out,valuetype)
        if i==16:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3active_energy_in=read_date.decode("utf-8")
           print ('L3 Aktive Effekt in', L3active_energy_in,valuetype)
        if i==17:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1reactive_energy_out=read_date.decode("utf-8")
           print ('L1 reaktiv Effekt uttag', L1reactive_energy_out,valuetype)
        if i==18:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1reactive_energy_in=read_date.decode("utf-8")
           print ('L1 reaktive Effekt in', L1reactive_energy_in,valuetype)
        if i==19:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2reactive_energy_out=read_date.decode("utf-8")
           print ('L2 reaktiv Effekt uttag', L2reactive_energy_out,valuetype)
        if i==20:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2reactive_energy_in=read_date.decode("utf-8")
           print ('L2 reaktive Effekt in', L2reactive_energy_in,valuetype)
        if i==21:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3reactive_energy_out=read_date.decode("utf-8")
           print ('L3 reaktiv Effekt uttag', L3reactive_energy_out,valuetype)
        if i==22:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3reactive_energy_in=read_date.decode("utf-8")
           print ('L3 reaktive Effekt in', L3reactive_energy_in,valuetype)
        if i==23:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1voltage=read_date.decode("utf-8")
           print ('Fasspänning L1', L1voltage, valuetype)
        if i==24:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2voltage=read_date.decode("utf-8")
           print ('Fasspänning L2', L2voltage,valuetype)
        if i==25:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3voltage=read_date.decode("utf-8")
           print ('Fasspänning L3', L3voltage,valuetype)
        if i==26:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1ampere=read_date.decode("utf-8")
           print ('Fasström L1', L1ampere, valuetype)
        if i==27:
           read_date =read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2ampere=read_date.decode("utf-8")
           print ('Fasström L2', L2ampere,valuetype)
        if i==28:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3ampere=read_date.decode("utf-8")
           print ('Fasström L3', L3ampere,valuetype)
    else:
        print("forloop finished")
    mqtt_save('Aktiv_energi',active_energy_out)
    mqtt_save('effektutag',active_energy_out_curr)
    mqtt_save('SpänningL1',L1voltage)
    mqtt_save('SpänningL2',L2voltage)
    mqtt_save('SpänningL3',L3voltage)
    mqtt_save('FasströmL2',L2ampere)
    mqtt_save('FasströmL2',L2ampere)
    mqtt_save('FasströmL3',L3ampere)

serial_port.close()
