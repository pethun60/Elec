#!/usr/bin/env python3
import serial
import paho.mqtt.client as mqtt
import logging
import time
import socket
import errno
import schedule


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


# define file handler and set formatter
file_handler = logging.FileHandler('error.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)


def mqtt_save():

    def on_connect(client, userdata, flags, rc):
        if rc==0:
            client.connected_flag=True #set flag
            print("connected OK")
            #logger.debug('connected OK to mqtt broker')
        else:
            print("Bad connection Returned code=",rc)
            logger.debug('Failed to connect to mqtt broker')

    #input_topic="/el/tobo/"
    #input_message=mqtt_value
    input_host="192.168.1.105"
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
        time.sleep(10)
    print("mqtt connected or failed")
    client.loop_stop()
    #client.publish(input_topic, input_message);
    input_topic="/el/tobo/"+"Aktiv_energi_mätare"
    client.publish(input_topic,active_energy_out)
    input_topic="/el/tobo/"+"aktiv effekt"
    client.publish(input_topic,active_energy_out_curr)
    input_topic="/el/tobo/"+"SpänningL1"
    client.publish(input_topic,L1voltage)
    input_topic="/el/tobo/"+"SpänningL2"
    client.publish(input_topic,L2voltage)
    input_topic="/el/tobo/"+"SpänningL3"
    client.publish(input_topic,L3voltage)
    input_topic="/el/tobo/"+"FasströmL1"
    client.publish(input_topic,L1ampere)
    input_topic="/el/tobo/"+"FasströmL2"
    client.publish(input_topic,L2ampere)
    input_topic="/el/tobo/"+"FasströmL3"
    client.publish(input_topic,L3ampere)
    client.disconnect();
    #logger.debug('all mqtt_save value saved')
    #f= open("temp_RH.txt","a+")
    #f.write("mqtt value" + mqtt_value + "\n")
    #f.write(input_topic +"\n")
    #f.close()

def hourly_energy():
    #save energy consumption every hour
    now = time.localtime()
    current_time = time.strftime("%H:%M:%S", now)
    logger.debug('hourly energy function run ', current_time)
    print("hourly energy output")

# -------------------------------------------------


if __name__ == '__main__':
    # Used when called directly
    
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

    #scheduler = sched.scheduler(time.time, time.sleep)
    schedule.every(60).seconds.do(hourly_energy)

   

    # serial_port.open()
    while True:
        try: 
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
                    #print ('date', datevalue)
                if i==3:
                    #print("startpos", pos_start)
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    active_energy_out=read_date.decode("utf-8")
                    #print ('active energiuttag  mätare',active_energy_out,valuetype)
                if i==4:
                    #print("rad 4")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    active_energy_in=read_date.decode("utf-8")
                    #print ('active energi inmatning mätare', active_energy_in,valuetype)
                if i==5:
                    #print("rad 5")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    reactive_energy_out=read_date.decode("utf-8")
                    #print ('reactive energi uttag', reactive_energy_out,valuetype)
                if i==6:
                    #print("rad 6")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    reactive_energi_in=read_date.decode("utf-8")
                    #print ('reactive energi inmatning', reactive_energi_in,valuetype )
                if i==7:
                    #print("rad 7aktiv")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    active_energy_out_curr=read_date.decode("utf-8")
                    #print ('aktiv effekt uttag', active_energy_out_curr,valuetype)
                if i==8:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    active_energy_in_curr=read_date.decode("utf-8")
                    #print ('aktiv effekt inmatning', active_energy_in_curr,valuetype)
                if i==9:
                    #print("rad 7aktiv")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    reactive_energy_out_curr=read_date.decode("utf-8")
                    #print ('reaktiv effekt uttag', reactive_energy_out_curr,valuetype)
                if i==10:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    reactive_energy_in_curr=read_date.decode("utf-8")
                    #print ('reaktiv effekt inmatning', reactive_energy_in_curr,valuetype)
                if i==11:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L1active_energy_out=read_date.decode("utf-8")
                    #print ('L1 Aktiv Effekt uttag', L1active_energy_out,valuetype)
                if i==12:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L1active_energy_in=read_date.decode("utf-8")
                    #print ('L1 Aktive Effekt in', L1active_energy_in,valuetype)
                if i==13:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L2active_energy_out=read_date.decode("utf-8")
                    #print ('L2 Aktiv Effekt uttag', L2active_energy_out,valuetype)
                if i==14:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L2active_energy_in=read_date.decode("utf-8")
                    #print ('L2 Aktive Effekt in', L2active_energy_in,valuetype)
                if i==15:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L3active_energy_out=read_date.decode("utf-8")
                    #print ('L3 Aktiv Effekt uttag', L3active_energy_out,valuetype)
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
                    #print ('L1 reaktive Effekt in', L1reactive_energy_in,valuetype)
                if i==19:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L2reactive_energy_out=read_date.decode("utf-8")
                    #print ('L2 reaktiv Effekt uttag', L2reactive_energy_out,valuetype)
                if i==20:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L2reactive_energy_in=read_date.decode("utf-8")
                    #print ('L2 reaktive Effekt in', L2reactive_energy_in,valuetype)
                if i==21:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L3reactive_energy_out=read_date.decode("utf-8")
                    #print ('L3 reaktiv Effekt uttag', L3reactive_energy_out,valuetype)
                if i==22:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L3reactive_energy_in=read_date.decode("utf-8")
                    #print ('L3 reaktive Effekt in', L3reactive_energy_in,valuetype)
                if i==23:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L1voltage=read_date.decode("utf-8")
                    #print ('Fasspänning L1', L1voltage, valuetype)
                if i==24:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L2voltage=read_date.decode("utf-8")
                    #print ('Fasspänning L2', L2voltage,valuetype)
                if i==25:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L3voltage=read_date.decode("utf-8")
                    #print ('Fasspänning L3', L3voltage,valuetype)
                if i==26:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L1ampere=read_date.decode("utf-8")
                    #print ('Fasström L1', L1ampere, valuetype)
                if i==27:
                    read_date =read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L2ampere=read_date.decode("utf-8")
                    #print ('Fasström L2', L2ampere,valuetype)
                if i==28:
                    #print("rad 8")
                    read_date = elec_data[pos_start:pos_end]
                    valuetype = elec_data[pos_end+1:pos_type]
                    L3ampere=read_date.decode("utf-8")
                    #print ('Fasström L3', L3ampere,valuetype)
            else:
                print("forloop finished")
            mqtt_save()
            schedule.run_pending()
            #scheduler.enter(60, 1, hourly_energy, ())
            # test code
            #scheduler.run()

    #mqtt_save('effektutag',active_energy_out_curr)
    #mqtt_save('SpänningL1',L1voltage)
    #mqtt_save('SpänningL2',L2voltage)
    #mqtt_save('SpänningL3',L3voltage)
    #mqtt_save('FasströmL2',L2ampere)
    #mqtt_save('FasströmL2',L2ampere)
    #mqtt_save('FasströmL3',L3ampere)
    #serial_port.close()
        except socket.error as e:
            print(repr(e))
            logger.debug(repr(e))
            if  e.errno == 101:
                logger.error("error in network will wait 10s")
                print("error netverket är otillgängligt")
                time.sleep(10)
                continue
            #if socket.timeout
            #    logger.debug("timeout error in network" 
            #    time.sleep(10)
            #    continue  
            #else:
                #(f"socket error: {e}")
            #    print ("error no=" +e)
            #    logger.error("error " +e)
            #    serial_port.close()
            #    break
        except socket.timeout:
            logger.error("timeout error in network")
            print("Socket timeout occurred.") 
            time.sleep(11)
            continue
