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
from Library.B1_jsonFileControl.jsonFileControl import jsonFileRecord
import threading
import copy
import re

NODE_MANAGER_FILE = "/myConfig/nodeManagement.json"
NODE_MAN = jsonFileRecord()
nodeManJson = dict(NODE_MAN.loadFromJsonFile(NODE_MANAGER_FILE))

messageNum = 0 #Message counter number

#Controller struct type
#  "controllerUid": "DeviceUID1",
#  "channel1": "AUTO_OFF",
#  "channel1_info": "",
#  "channel1_lock": "",
#  "channel2": "AUTO_ON",
#  "channel2_info": "",
#  "channel2_lock": "",
#  "channel3": "MANUAL_ON",
#  "channel3_info": "MANUAL ON",
#  "channel3_lock": "locked",
#  "channel4": "MANUAL_OFF",
#  "channel4_info": "MANUAL OFF",
#  "channel4_lock": "locked"
#}
controllerStr = {
  "info" : {
    "controllerUid": "deviceUID",
    "controllerName": "CONTROLLER NODE",
    "channel1": "AUTO_OFF",
    "channel1_alias": "channel1",
    "channel1_info": "",
    "channel1_lock": "",
    "channel2": "AUTO_OFF",
    "channel2_alias": "channel2",
    "channel2_info": "",
    "channel2_lock": "",
    "channel3": "AUTO_OFF",
    "channel3_alias": "channel3",
    "channel3_info": "",
    "channel3_lock": "",
    "channel4": "AUTO_OFF",
    "channel4_alias": "channel4",
    "channel4_info": "",
    "channel4_lock": ""
  },
  "scheduleList": []
}

#Schedule struct type
scheduleStr = {
  "scheduleUid": 1,
  "channel": 1,
  "title": "Schedule 1",
  "action": "on",
  "fromDate": "2020-01-01",
  "fromTime": "10:10",
  "repeat": "daily",
  "daysOfWeek": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  "untilDate": "2020-12-31"
}

#########################################################################################
# B. MQTT PART
#########################################################################################
############################################################
# 1. CONNECT TO MQTT BROKER                                #
############################################################
MQTT = mqttClass(MQTT_BROKER_IP, MQTT_PORT, MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD)
def subcribeFilter(msg):
  global messageNum
  messageNum += 1
  networkType = ""
  try:
    topic = str(msg.topic)
    gwName = topic.split(".")[0]
    gwUid = gwName.split("_")[2]
    jsonData = eval(str(msg.payload.decode()))
    
    if "uid" in jsonData and "SIO_EXCTL" in jsonData["uid"]: #Message in socketio network
      fullMessage = eval(str(jsonData["message"]))
      networkType = "SOCKETIO"
    else:
      fullMessage = jsonData #Message in mqtt network only
      networkType = "MQTT"
    
    ### MESSAGE IN SOCKETIO NETWORK ####
    if networkType == "SOCKETIO":
      ########################
      ### MESSAGE CHECKING ###
      ########################
      #### A. FROM DASHBOARD ####
      #A1. Load request at first time/peiordically
      if "control.get" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\n\n\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.get\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m")
        __checkExistProfile(controllerUid,gwName) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        __sendAllChannelStatus(controllerUid,topic,gwName) #Sync to every web clients
        
      #A2. Update channel status from WEB GUI
      if "control.post" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.post\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m\n\n")
        __checkExistProfile(controllerUid,gwName) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        
        #For each key in fullMessage["params"], update to nodeManJson[gwName]["NODE_"+controllerUid]["info"]
        for key in fullMessage["params"]:
          if key != "controllerUid":
            #Extract channel number from key
            #Kiểm tra REGEX của key có phải là channel[0-9] không?
            if re.match(r"^channel[0-9]$", key):
              channelNum = int(key.split("channel")[1])
              channelStatus = fullMessage["params"][key]
              
            nodeManJson[gwName]["NODE_"+controllerUid]["info"][key] = fullMessage["params"][key]

        
        print(f'\x1b[48;5;1m <<<<< Receive Updated Status[Num: {messageNum}]\x1b[48;5;21m[TOPIC: {topic}]\n\x1b[48;5;1m[Message]\x1b[0m\x1b[0m\x1b[38;5;3m {fullMessage}\x1b[0m')
        __sendAllChannelStatus(controllerUid,topic,gwName) #Sync to every web clients
        #Update to file
        NODE_MAN.syncToJsonFile(fileName=NODE_MANAGER_FILE, profileManager=nodeManJson)

        
      #### B. FROM SCHEDULE LIST ####
      #A1. Load all schedule request at first time/peiordically
      if "control.schedule.loadAll" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\n\n\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.schedule.loadAll\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m")
        __checkExistProfile(controllerUid,gwName) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        __sendAllScheduleList(controllerUid,topic,gwName) #Send all schedule list to web client

      #A2. Add new schedule
      if "control.schedule.add" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\n\n\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.schedule.add\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m")
        __checkExistProfile(controllerUid,gwName) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        #Send all schedule list to web client
        print("Add new schedule to controllerUid: "+str(fullMessage))
        nodeManJson[gwName]["NODE_"+controllerUid]["scheduleList"].append(fullMessage["params"]["schedule"])
        #Update to file
        NODE_MAN.syncToJsonFile(fileName=NODE_MANAGER_FILE, profileManager=nodeManJson)
        #Send all schedule list to web client
        __sendAllScheduleList(controllerUid,topic,gwName) #Send all schedule list to web client


      #A3. Modify schedule
      if "control.schedule.modify" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\n\n\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.schedule.modify\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m")
        __checkExistProfile(controllerUid,gwName) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        #Send all schedule list to web client
        print("Modify schedule to controllerUid: "+str(fullMessage))
        for schedule in nodeManJson[gwName]["NODE_"+controllerUid]["scheduleList"]:
          if schedule["scheduleUid"] == fullMessage["params"]["schedule"]["scheduleUid"]:
            #Update fullMessage["params"]["schedule"] to schedule in nodeManJson
            schedule.update(fullMessage["params"]["schedule"])
            break
        #Update to file
        NODE_MAN.syncToJsonFile(fileName=NODE_MANAGER_FILE, profileManager=nodeManJson)
        #Send all schedule list to web client
        __sendAllScheduleList(controllerUid,topic,gwName) #Send all schedule list to web client


      #A4. Remove schedule
      if "control.schedule.remove" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\n\n\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.schedule.remove\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m")
        __checkExistProfile(controllerUid,gwName) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        #Send all schedule list to web client
        print("Remove schedule to controllerUid: "+str(fullMessage))
        for schedule in nodeManJson[gwName]["NODE_"+controllerUid]["scheduleList"]:
          if int(schedule["scheduleUid"]) == int(fullMessage["params"]["scheduleUid"]):
            #Update fullMessage["params"]["schedule"] to schedule in nodeManJson
            nodeManJson[gwName]["NODE_"+controllerUid]["scheduleList"].remove(schedule)
            break
        #Update to file
        NODE_MAN.syncToJsonFile(fileName=NODE_MANAGER_FILE, profileManager=nodeManJson)
        #Send all schedule list to web client
        __sendAllScheduleList(controllerUid,topic,gwName) #Send all schedule list to web client
        
        
    #### FROM GATEWAY ####
    ### MESSAGE IN MQTT NETWORK ONLY ####
    if networkType == "MQTT":
      if "GATEWAY.CONTROL" in topic: #Message from gateway to update the controller node status on web
        #TOPIC: WSN_GW_01C823.GATEWAY.CONTROL
        #MESSAGE: {"gatewayUID": "01C823", "controllerUid": "DeviceUID1", "channelNum": 1, "channelStatus": "AUTO_ON"}
        fullMessage = fullMessage["message"]
        print(f'Get request from Gateway to update controller status on web.\n[Topic: {topic}][Message] {fullMessage}')
        controllerUid = fullMessage["params"]["controllerUid"]
        __checkExistProfile(controllerUid,gwName) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        #Update control management from data received from gateway
        for key in fullMessage["params"]:
          print("DEBUG: "+str(key))
          if key != "controllerUid":
            #Extract channel number from key
            #Kiểm tra REGEX của key có phải là channel[0-9] không?
            if re.match(r"^channel[0-9]$", key):
              updateValue = fullMessage["params"][key]
              if updateValue == "AUTO_ON" or updateValue == "AUTO_OFF":
                nodeManJson[gwName]["NODE_"+controllerUid]["info"][key] = fullMessage["params"][key]
                nodeManJson[gwName]["NODE_"+controllerUid]["info"][key+"_info"] = ""
                nodeManJson[gwName]["NODE_"+controllerUid]["info"][key+"_lock"] = ""
              elif updateValue == "MANUAL_ON":
                nodeManJson[gwName]["NODE_"+controllerUid]["info"][key] = fullMessage["params"][key]
                nodeManJson[gwName]["NODE_"+controllerUid]["info"][key+"_info"] = "MANUAL ON"
                nodeManJson[gwName]["NODE_"+controllerUid]["info"][key+"_lock"] = "locked"
              elif updateValue == "MANUAL_OFF":
                nodeManJson[gwName]["NODE_"+controllerUid]["info"][key] = fullMessage["params"][key]
                nodeManJson[gwName]["NODE_"+controllerUid]["info"][key+"_info"] = "MANUAL OFF"
                nodeManJson[gwName]["NODE_"+controllerUid]["info"][key+"_lock"] = "locked"
              else:
                pass
              
                
                
                
                
              
        
        
        
        

        #Send all schedule list to web client
        __sendAllChannelStatus(controllerUid,topic.replace("GATEWAY","WEB"),gwName) #Sync to every web clients
        #Update to file
        NODE_MAN.syncToJsonFile(fileName=NODE_MANAGER_FILE, profileManager=nodeManJson)
        
      
      
      
      
      
  except Exception as e:
    print("ERROR: "+str(e))
    pass
        
def __checkExistProfile(controllerUid="",gwName="WSN_GW_01C823"):
  if gwName in nodeManJson:
    pass
  else:
    nodeManJson[gwName] = dict()
  
  if "NODE_"+controllerUid in nodeManJson[gwName]:
    pass
  else:
    nodeManJson[gwName]["NODE_"+controllerUid] = copy.deepcopy(controllerStr)
    #Update controllerUid
    nodeManJson[gwName]["NODE_"+controllerUid]["info"]["controllerUid"] = controllerUid
    print("Create new profile for controllerUid: "+str(controllerUid))
    #Update to file
    NODE_MAN.syncToJsonFile(fileName=NODE_MANAGER_FILE, profileManager=nodeManJson)

def __sendAllChannelStatus(controllerUid="", topic="",gwName="WSN_GW_01C823"):
  #Sync to every web clients
  messageContent = nodeManJson[gwName]["NODE_"+controllerUid]["info"]
  responseMessage = {"uid": str(MQTT_CLIENT_ID), "message": {"method": "control.get", "params": messageContent}}
  print(f'\x1b[48;5;2m >>>>> Publish MQTT [Num: {messageNum}]\x1b[48;5;21m[TOPIC: {topic}]\n\x1b[48;5;2m[Message]\x1b[0m\x1b[0m\x1b[38;5;3m {responseMessage}\x1b[0m')
  MQTT.publish(str(topic), str(responseMessage))
        
def __sendAllScheduleList(controllerUid="", topic="",gwName="WSN_GW_01C823"):
  messageContent = nodeManJson[gwName]["NODE_"+controllerUid]["scheduleList"]
  responseMessage = {"uid": str(MQTT_CLIENT_ID), "message": {"method": "control.schedule.loadAll", "params": {"scheduleList":messageContent}}}
  print(f'\x1b[48;5;2m >>>>> Publish MQTT [Num: {messageNum}]\x1b[48;5;21m[TOPIC: {topic}]\n\x1b[48;5;2m[Message]\x1b[0m\x1b[0m\x1b[38;5;3m {responseMessage}\x1b[0m')
  MQTT.publish(str(topic), str(responseMessage))
          
#Subscribe all accepted topic
for gateway in ACCEPT_LIST_OF_GATEWAY:
  for acceptTopic in ACCEPT_LIST_OF_TOPIC:
    if acceptTopic == "WEB.CONTROL" or acceptTopic == "GATEWAY.CONTROL":
      MQTT.subscribe(gateway+"."+acceptTopic)
MQTT.msgRcvFilter = subcribeFilter

#########################################################################################
# C. ZABBIX PART
#########################################################################################











#########################################################################################
threading.Thread(target=MQTT.listen).start()
print("===== DONE =====")