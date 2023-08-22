import __init
############ IMPORT PARAMETER ############
import sys,os
if os.path.exists("/myConfiguration.py"): #Mapped from host to container
  MAIN_WORKDIR = os.path.dirname(sys.path[0])
  os.system("cp /myConfiguration.py "+MAIN_WORKDIR+"/cloneMyConfig.py")
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
import wget
        
#########################################################################################
# A. SOCKETIO PART
#########################################################################################
sio = socketio.Client()

@sio.event(namespace='/ZABBIX')
def SOCKET(data:dict):
  #1.Convert data to JSON
  if type(data) == str:
    message = json.loads(data)
  elif type(data) == dict:
    message = data
  else:
    print("[SOCKET] Received message is not string or dict => Skip message")
    return
  if 'method' in message.keys():
    method = message['method']
  else:
    print("[SOCKET] Received message has no 'method' key => Skip message")
    return
  if 'params' in message.keys():
    params = message['params']
  else:
    print("[SOCKET] Received message has no 'method' key => Skip message")
    return
  ###############################
  #2. Check method
  ###############################
  #2.1. Check "problem.get"
  if method == "problem.get":
    getThenSendHostGroupProblem(params["hostgroupName"],params["topic"])
    
  
  
SOCKETIO_URL = "http://lotus_socketio:5000" # EX: "http://lotus1104.synology.me:83"
sio.connect(SOCKETIO_URL,namespaces=['/ZABBIX'])

#########################################################################################
# A. SOCKETIO PART
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
      

      
      #Download from a link
      print(URL)
      wget()
      wget.download(URL, f'./ABC.png')






MQTT.subscribe(MQTT_TOPIC)
MQTT.msgRcvFilter = subcribeFilter
threading.Thread(target=MQTT.listen).start()


#########################################################################################
# ZABBIX PART
#########################################################################################
zabbixLib = ZABBIX_LIB(ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_USER, ZABBIX_PASS, ZABBIX_URL)
def getHostGroupProblem(hostgroupName):
  group_id = zabbixLib.getHostGroupID(hostgroupName)
  hostGroupProblem = zabbixLib.checkGroupProblem(group_id,ZABBIX_SERVER)
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
print("===== START =====")
# getThenSendHostGroupProblem("SeasideConsulting_GW01C821","WSN_GW_01C821")

#Kiểm tra thư mục /HShare/ có file ZabbixReq không?
#Nếu có thì load hết nội dung của file vào một biến data tạm thời. Sau đó xóa file ZabbixReq.
#Tiến hành đọc từng dòng của biến data tạm thời
#Nếu dòng nào có lineData["method"] là "problem.get" thì gọi hàm getThenSendHostGroupProblem(lineData["params"]["hostgroupName"],lineData["params"]["topic"])
#Nếu không thì bỏ qua
# import os
# import time

# os.system("touch /HShare/ZabbixReq")
# os.system("echo '{\"method\":\"problem.get\",\"params\":{\"hostgroupName\":\"SeasideConsulting_GW01C821\",\"topic\":\"WSN_GW_01C821\"}}' >> /HShare/ZabbixReq")

# while True:
#   if os.path.exists("/HShare/ZabbixReq"):
#     print("===== ZabbixReq FOUND =====")
#     with open("/HShare/ZabbixReq","r") as f:
#       data = f.read()
#       f.close()
#     os.remove("/HShare/ZabbixReq")
#     for line in data.split("\n"):
#       if line == "":
#         continue
#       lineData = eval(line)
#       try:
#         #1. Request "problem.update"
#         if lineData["method"] == "problem.get":
#           getThenSendHostGroupProblem(lineData["params"]["hostgroupName"],lineData["params"]["topic"])
#         #2. Request others
#         
#       except Exception as e:
#         print(e)
#  time.sleep(0.001)





print("===== DONE =====")

#http://157.65.24.169/zabbix.php?show=3&show_timeline=1&action=problem.view&groupids%5B%5D=38&hostids%5B%5D=10593