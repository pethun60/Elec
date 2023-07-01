import paho.mqtt.client as mqtt

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
