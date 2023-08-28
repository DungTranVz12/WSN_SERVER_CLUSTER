import __init
############ IMPORT PARAMETER ############
import sys,os
if os.path.exists("/0_SHARE/myConfiguration.py"): #Mapped from host to container
  MAIN_WORKDIR = sys.path[0]
  os.system("cp /0_SHARE/myConfiguration.py "+MAIN_WORKDIR+"/cloneMyConfig.py")
  from cloneMyConfig import *
else:
  from Application.parameter import *
##########################################
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX_LIB
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt
import threading
import pprint

#########################################################################################
# B. MQTT PART
#########################################################################################
############################################################
# 1. CONNECT TO MQTT BROKER                                #
############################################################
MQTT = mqttClass(MQTT_BROKER_IP, MQTT_PORT, MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD)
def subcribeFilter(msg):
  try:
    jsonData = eval(str(msg.payload.decode()))
    message = eval(str(jsonData["message"]))
    # print(jsonData)
    if "SIO_EXCTL" in jsonData["uid"] and "problem.get" in message["method"]:
      print(message["params"]["hostgroupName"])
      problemResult = getHostGroupProblem(hostgroupName=message["params"]["hostgroupName"])
      if problemResult == False:
        print("ERROR: Cannot get problem from Zabbix")
        return False
      else:
        # pprint.pprint(problemResult)
        topic=message["params"]["topic"]
        message={
          "uid": str(MQTT_CLIENT_ID),
          "message":{
            "method": "problem.update",
            "params": problemResult
          }
        }
        MQTT.publish(str(topic), str(message))
      
  except Exception as e:
    print("ERROR: "+str(e))
    pass
    

      

#Subscribe all accept topic
for gateway in ACCEPT_LIST_OF_GATEWAY:
  for acceptTopic in ACCEPT_LIST_OF_TOPIC:
    if acceptTopic == "WEB.SCAN_PROBLEM":
      MQTT.subscribe(gateway+"."+acceptTopic)
MQTT.msgRcvFilter = subcribeFilter
threading.Thread(target=MQTT.listen).start()


#########################################################################################
# C. ZABBIX PART
#########################################################################################
zabbixLib = ZABBIX_LIB(ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_USER, ZABBIX_PASS, ZABBIX_URL)
def getHostGroupProblem(hostgroupName):
  group_id = zabbixLib.getHostGroupID(hostgroupName)
  if group_id == False:
    return False
  hostGroupProblem = zabbixLib.checkGroupProblem(group_id,ZABBIX_WEB_OUTSIDE_IP_PORT)
  return hostGroupProblem
##################################################################################################
print("===== DONE =====")