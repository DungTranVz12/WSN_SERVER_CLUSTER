import __init
############ IMPORT PARAMETER ############
from Application.parameter import *
import sys,os
if os.path.exists("/myConfiguration.py"): #Mapped from host to container
  MAIN_WORKDIR = os.path.dirname(sys.path[0])
  os.system("cp /myConfiguration.py "+MAIN_WORKDIR+"/cloneMyConfig.py")
  from cloneMyConfig import *
##########################################
import socketio
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt
import threading
import random
import json


############################################################
# 1. CONNECT TO MQTT BROKER                                #
############################################################
MQTT = mqttClass(MQTT_BROKER_IP, MQTT_PORT, MQTT_CLIENT_MQTT_EXCTL_ID, MQTT_USERNAME, MQTT_PASSWORD)
def subcribeFilter(msg):
  jsonData = eval(msg.payload.decode())
  #Check sender uid
  if "SIO_EXCTL" in jsonData["uid"]: return #SOCKETIO_EXPORT_CONTROL
  #CHECK LICENSE
  if msg.topic in SOCKETIO_EXPORT_LICENSE_TOPIC_LIST:
    #SEND TO SOCKETIO
    sio.emit('SOCKET', {"topic":msg.topic,"message":jsonData["message"]},namespace='/MQTT')
for subTopic in SOCKETIO_EXPORT_LICENSE_TOPIC_LIST: #Subcribe to all topic in SOCKETIO_EXPORT_LICENSE_TOPIC_LIST
  MQTT.subscribe(subTopic)
MQTT.msgRcvFilter = subcribeFilter
threading.Thread(target=MQTT.listen).start()
##############################################################
############################################################
# 2. CONNECT TO SOCKETIO BROKER                            #
############################################################
sio = socketio.Client()
sio.connect(SOCKETIO_URL,namespaces=['/MQTT'])
    