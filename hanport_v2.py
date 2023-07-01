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
           datevalue=read_date  
           print ('date', datevalue)
        if i==3:
           print("startpos", pos_start)
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           active_energy_out=read_date  
           print ('active energiuttag  mätare',active_energy_out,valuetype)
        if i==4:
           #print("rad 4")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           active_energy_in=read_date  
           print ('active energi inmatning mätare', active_energy_in,valuetype)
        if i==5:
           #print("rad 5")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           reactive_energy_out=read_date  
           print ('reactive energi uttag', reactive_energy_out,valuetype)
        if i==6:
           #print("rad 6")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           reactive_energi_in=read_date  
           print ('reactive energi inmatning', reactive_energi_in,valuetype )
        if i==7:
           #print("rad 7aktiv")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           active_energy_out_curr=read_date  
           print ('aktiv effekt uttag', active_energy_out_curr,valuetype)
        if i==8:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           active_energy_in_curr=read_date  
           print ('aktiv effekt inmatning', active_energy_in_curr,valuetype)
        if i==9:
           #print("rad 7aktiv")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           reactive_energy_out_curr=read_date  
           print ('reaktiv effekt uttag', reactive_energy_out_curr,valuetype)
        if i==10:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           reactive_energy_in_curr=read_date  
           print ('reaktiv effekt inmatning', reactive_energy_in_curr,valuetype)
        if i==11:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1active_energy_out=read_date  
           print ('L1 Aktiv Effekt uttag', L1active_energy_out,valuetype)
        if i==12:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1active_energy_in=read_date  
           print ('L1 Aktive Effekt in', L1active_energy_in,valuetype)
        if i==13:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2active_energy_out=read_date  
           print ('L2 Aktiv Effekt uttag', L2active_energy_out,valuetype)
        if i==14:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2active_energy_in=read_date  
           print ('L2 Aktive Effekt in', L2active_energy_in,valuetype)
        if i==15:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3active_energy_out=read_date  
           print ('L3 Aktiv Effekt uttag', L3active_energy_out,valuetype)
        if i==16:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3active_energy_in=read_date  
           print ('L3 Aktive Effekt in', L3active_energy_in,valuetype)
        if i==17:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1reactive_energy_out=read_date  
           print ('L1 reaktiv Effekt uttag', L1reactive_energy_out,valuetype)
        if i==18:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1reactive_energy_in=read_date  
           print ('L1 reaktive Effekt in', L1reactive_energy_in,valuetype)
        if i==19:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2reactive_energy_out=read_date  
           print ('L2 reaktiv Effekt uttag', L2reactive_energy_out,valuetype)
        if i==20:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2reactive_energy_in=read_date  
           print ('L2 reaktive Effekt in', L2reactive_energy_in,valuetype)
        if i==21:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3reactive_energy_out=read_date  
           print ('L3 reaktiv Effekt uttag', L3reactive_energy_out,valuetype)
        if i==22:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3reactive_energy_in=read_date  
           print ('L3 reaktive Effekt in', L3reactive_energy_in,valuetype)
        if i==23:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1voltage=read_date  
           print ('Fasspänning L1', L1voltage, valuetype)
        if i==24:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2voltage=read_date  
           print ('Fasspänning L2', L2voltage,valuetype)
        if i==25:   
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3voltage=read_date  
           print ('Fasspänning L3', L3voltage,valuetype)
        if i==26:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L1ampere=read_date  
           print ('Fasström L1', L1ampere, valuetype)
        if i==27:
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L2ampere=read_date  
           print ('Fasström L2', L2ampere,valuetype)
        if i==28:   
           #print("rad 8")
           read_date = elec_data[pos_start:pos_end]
           valuetype = elec_data[pos_end+1:pos_type]
           L3ampere=read_date  
           print ('Fasström L3', L3ampere,valuetype)
    else:
        print("forloop finished") 
# do something


serial_port.close()
