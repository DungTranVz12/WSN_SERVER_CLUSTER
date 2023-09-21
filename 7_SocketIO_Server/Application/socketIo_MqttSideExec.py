import __init
############ IMPORT PARAMETER ############
import os,time
import re
time.sleep(1) #Chờ cho server khởi động và copy file cloneMyConfig.py vào /AppDir/cloneMyConfig.py
if os.path.exists("/myConfig/myConfigWSN.py"): #Mapped from host to container
  from cloneMyConfig import *
else:
  from Application.parameter import *
##########################################
import socketio
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt
import threading
import time

while True:
  try:
    ############################################################
    # 1. CONNECT TO MQTT BROKER                                #
    ############################################################
    MQTT = mqttClass(MQTT_BROKER_IP, MQTT_PORT, MQTT_CLIENT_MQTT_EXCTL_ID, MQTT_USERNAME, MQTT_PASSWORD)
    def subcribeFilter(msg):
      jsonData = eval(msg.payload.decode())
      #Check sender uid
      print (jsonData["uid"])
      if "SIO_EXCTL" in jsonData["uid"]: return #SOCKETIO_EXPORT_CONTROL
      #CHECK LICENSE
      for regex in EXPORT_LICENSE_TO_SOCKETIO_TOPIC_LIST:
        if re.search(regex, msg.topic):
          sio.emit('SOCKET', {"topic":msg.topic,"message":jsonData["message"]},namespace='/MQTT')
          break
    
    #Subscribe all accept topic
    for gateway in ACCEPT_LIST_OF_GATEWAY:
      for acceptTopic in ACCEPT_LIST_OF_TOPIC:
        if acceptTopic == "":
          MQTT.subscribe(gateway)
        else:
          MQTT.subscribe(gateway+"."+acceptTopic)
        
    MQTT.msgRcvFilter = subcribeFilter
    threading.Thread(target=MQTT.listen).start()
    ##############################################################
    ############################################################
    # 2. CONNECT TO SOCKETIO BROKER                            #
    ############################################################
    sio = socketio.Client(
      # reconnection=True,            # Cho phép kết nối lại
      # reconnection_attempts=10000,  # Số lần thử kết nối lại tối đa
      # reconnection_delay=1000,      # Độ trễ giữa các lần thử kết nối lại (milliseconds)
      # reconnection_delay_max=5000,  # Độ trễ tối đa giữa các lần thử kết nối lại
      # randomization_factor=0.5      # Hệ số ngẫu nhiên để ngăn chặn việc đồng loạt thử kết nối lại
    )
    sio.connect(SOCKETIO_URL,namespaces=['/MQTT'])
    print("Connected to SOCKETIO")
    #Check connection
    while True:
      time.sleep(5)
      if sio.connected == False:
        print("Disconnected to SOCKETIO")
        MQTT.disconnect()
        sio.disconnect()
        time.sleep(5)
        break
  except Exception as e:
    print (e)
    print("Disconnected to SOCKETIO")
    MQTT.disconnect()
    sio.disconnect()
    time.sleep(5)
    continue


    
    