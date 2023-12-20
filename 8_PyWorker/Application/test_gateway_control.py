import __init
############ IMPORT PARAMETER ############
import sys,os
if os.path.exists("/myConfig/myConfigWSN.py"): #Mapped from host to container
  MAIN_WORKDIR = sys.path[0]
  os.system("cp /myConfig/myConfigWSN.py "+MAIN_WORKDIR+"/cloneMyConfig.py")
  from cloneMyConfig import *
else:
  from Application.parameter import *
##########################################
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt

#### 1. Publish to a topic ####
import time

MQTT = mqttClass(MQTT_BROKER_IP, MQTT_PORT, MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD)

def channelControl(gatewayUID="", controllerUid="", channelNum=0, swithStatus="AUTO"):
  topic = "WSN_GW_"+gatewayUID+".GATEWAY.CONTROL"
  messageContent = {"gatewayUID": gatewayUID, "controllerUid": controllerUid, "channelNum": channelNum, "swithStatus": swithStatus}
  dataTime = time.strftime("%c")
  # Print datetime, topic, uid, channelNum, swithStatus
  print(f'[{dataTime}][TOPIC: {topic}][UID: {messageContent["controllerUid"]}][Channel: {messageContent["channelNum"]}][STATUS: {messageContent["swithStatus"]}]')
  MQTT.publish(str(topic), str(messageContent))

while True:
    DELAY_TIME = 1
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=1, swithStatus="AUTO");time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=2, swithStatus="AUTO");time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=3, swithStatus="AUTO");time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=4, swithStatus="AUTO");time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=1, swithStatus="OFF" );time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=2, swithStatus="OFF" );time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=3, swithStatus="OFF" );time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=4, swithStatus="OFF" );time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=1, swithStatus="ON"  );time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=2, swithStatus="ON"  );time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=3, swithStatus="ON"  );time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=4, swithStatus="ON"  );time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=1, swithStatus="OFF" );time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=2, swithStatus="OFF" );time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=3, swithStatus="OFF" );time.sleep(DELAY_TIME);
    channelControl(gatewayUID="01C823", controllerUid="DeviceUID1", channelNum=4, swithStatus="OFF" );time.sleep(DELAY_TIME);
