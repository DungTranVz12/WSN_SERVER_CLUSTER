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
import socketio
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX_LIB
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt
import threading
import pprint
import json

# #########################################################################################
# # A. SOCKETIO PART
# #########################################################################################
# sio = socketio.Client()

# @sio.event(namespace='/ZABBIX')
# def SOCKET(data:dict):
#   #1.Convert data to JSON
#   if type(data) == str:
#     message = json.loads(data)
#   elif type(data) == dict:
#     message = data
#   else:
#     print("[SOCKET] Received message is not string or dict => Skip message")
#     return
#   if 'method' in message.keys():
#     method = message['method']
#   else:
#     print("[SOCKET] Received message has no 'method' key => Skip message")
#     return
#   if 'params' in message.keys():
#     params = message['params']
#   else:
#     print("[SOCKET] Received message has no 'method' key => Skip message")
#     return
#   ###############################
#   #2. Check method
#   ###############################
#   #2.1. Check "problem.get"
#   if method == "problem.get":
#     getThenSendHostGroupProblem(params["hostgroupName"],params["topic"])
    

# sio.connect(SOCKETIO_URL,namespaces=['/ZABBIX'])

#########################################################################################
# B. MQTT PART
#########################################################################################
############################################################
# 1. CONNECT TO MQTT BROKER                                #
############################################################
MQTT = mqttClass(MQTT_BROKER_IP, MQTT_PORT, MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD)
def subcribeFilter(msg):
  jsonData = eval(str(msg.payload.decode()))
  if "method" in jsonData["alert.message"].keys():
    #META DATA
    eventDate     = jsonData["alert.message"]["params"]["event.date"]
    eventId       = jsonData["alert.message"]["params"]["event.id"]
    eventName     = jsonData["alert.message"]["params"]["event.name"]
    eventSeverity = jsonData["alert.message"]["params"]["event.severity"]
    eventTime     = jsonData["alert.message"]["params"]["event.time"]
    hostId        = jsonData["alert.message"]["params"]["host.id"]
    hostName      = jsonData["alert.message"]["params"]["host.name"]
    hostGroupName = jsonData["alert.message"]["params"]["hostgroup.name"]
    itemId        = jsonData["alert.message"]["params"]["item.id"]
    itemKey       = jsonData["alert.message"]["params"]["item.key"]
    itemName      = jsonData["alert.message"]["params"]["item.name"]
    itemValue     = jsonData["alert.message"]["params"]["item.value"]
    itemValueType = jsonData["alert.message"]["params"]["item.valuetype"]
    
    #1. Method "alert.send"
    if jsonData["alert.message"]["method"] == "alert.send":
      MTP = jsonData["alert.message"]["params"]["MTP"]
     
      URL = f'http://{ZABBIX_SERVER}/chart.php?&from=2023-06-25%2000%3A51%3A00&to=2023-06-25%2003%3A34%3A00&itemids%5B0%5D=44379&type=0&profileIdx=web.item.graph.filter&profileIdx2=44379&width=1082&height=300'
      
      ULR_LOGIN = 'http://157.65.24.169/index.php?name=Admin&password=zabbix&enter=Sign%20in'
      
      URL_GRAPH = 'http://157.65.24.169/chart.php?from=2023-06-25%2000%3A51%3A00&to=2023-06-25%2003%3A34%3A00&itemids%5B0%5D=44379&type=0&profileIdx=web.item.graph.filter&profileIdx2=44379&width=1082&height=300'
      

      







MQTT.subscribe(MQTT_TOPIC)
MQTT.msgRcvFilter = subcribeFilter
threading.Thread(target=MQTT.listen).start()


#########################################################################################
# C. ZABBIX PART
#########################################################################################
zabbixLib = ZABBIX_LIB(ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_USER, ZABBIX_PASS, ZABBIX_URL)
def getHostGroupProblem(hostgroupName):
  group_id = zabbixLib.getHostGroupID(hostgroupName)
  hostGroupProblem = zabbixLib.checkGroupProblem(group_id,ZABBIX_WEB_OUTSIDE_IP_PORT)
  return hostGroupProblem

def sendHostGroupProblem (topic:str,hostGroupProblem):
  message = {
    "method":"problem.update",
    "params": hostGroupProblem
  }
  sio.emit('SOCKET', {"topic":topic,"message":message},namespace='/ZABBIX')
  
def getThenSendHostGroupProblem(hostgroupName:str,topic:str):
  hostGroupProblem = getHostGroupProblem(hostgroupName)
  pprint.pprint(hostGroupProblem)
  sendHostGroupProblem(topic,hostGroupProblem)
##################################################################################################
print("===== DONE =====")