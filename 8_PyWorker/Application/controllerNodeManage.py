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
  try:
    topic = str(msg.topic)
    jsonData = eval(str(msg.payload.decode()))
    fullMessage = eval(str(jsonData["message"]))
    # print(jsonData)
    if "SIO_EXCTL" in jsonData["uid"]:
      ########################
      ### MESSAGE CHECKING ###
      ########################
      #### A. FROM DASHBOARD ####
      #A1. Load request at first time/peiordically
      if "control.get" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\n\n\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.get\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m")
        __checkExistProfile(controllerUid) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        
        messageContent = nodeManJson["NODE_"+controllerUid]["info"]
        responseMessage = {"uid": str(MQTT_CLIENT_ID), "message": {"method": "control.get", "params": messageContent}}
        print(f'\x1b[48;5;2m >>>>> Publish MQTT [Num: {messageNum}]\x1b[48;5;21m[TOPIC: {topic}]\n\x1b[48;5;2m[Message]\x1b[0m\x1b[0m\x1b[38;5;3m {responseMessage}\x1b[0m')
        MQTT.publish(str(topic), str(responseMessage))
        
      #A2. Update channel status from WEB GUI
      if "control.post" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.post\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m\n\n")
        __checkExistProfile(controllerUid) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        
        #Update control management
        nodeManJson["NODE_"+controllerUid]["info"] = fullMessage["params"]
        print(f'\x1b[48;5;1m <<<<< Receive Updated Status[Num: {messageNum}]\x1b[48;5;21m[TOPIC: {topic}]\n\x1b[48;5;1m[Message]\x1b[0m\x1b[0m\x1b[38;5;3m {fullMessage}\x1b[0m')
        #Sync to every web clients
        messageContent = nodeManJson["NODE_"+controllerUid]["info"]
        responseMessage = {"uid": str(MQTT_CLIENT_ID), "message": {"method": "control.get", "params": messageContent}}
        print(f'\x1b[48;5;2m >>>>> Publish MQTT [Num: {messageNum}]\x1b[48;5;21m[TOPIC: {topic}]\n\x1b[48;5;2m[Message]\x1b[0m\x1b[0m\x1b[38;5;3m {responseMessage}\x1b[0m')
        MQTT.publish(str(topic), str(responseMessage))
        #Update to file
        NODE_MAN.syncToJsonFile(fileName=NODE_MANAGER_FILE, profileManager=nodeManJson)
      
      #### B. FROM SCHEDULE LIST ####
      #A1. Load all schedule request at first time/peiordically
      if "control.schedule.loadAll" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\n\n\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.schedule.loadAll\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m")
        __checkExistProfile(controllerUid) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        #Send all schedule list to web client
        __sendAllScheduleList(controllerUid,topic) #Send all schedule list to web client

      #A2. Add new schedule
      if "control.schedule.add" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\n\n\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.schedule.add\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m")
        __checkExistProfile(controllerUid) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        #Send all schedule list to web client
        print("Add new schedule to controllerUid: "+str(fullMessage))
        nodeManJson["NODE_"+controllerUid]["scheduleList"].append(fullMessage["params"]["schedule"])
        #Update to file
        NODE_MAN.syncToJsonFile(fileName=NODE_MANAGER_FILE, profileManager=nodeManJson)
        #Send all schedule list to web client
        __sendAllScheduleList(controllerUid,topic) #Send all schedule list to web client

      #A3. Modify schedule
      if "control.schedule.modify" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\n\n\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.schedule.modify\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m")
        __checkExistProfile(controllerUid) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        #Send all schedule list to web client
        print("Modify schedule to controllerUid: "+str(fullMessage))
        for schedule in nodeManJson["NODE_"+controllerUid]["scheduleList"]:
          if schedule["scheduleUid"] == fullMessage["params"]["schedule"]["scheduleUid"]:
            #Update fullMessage["params"]["schedule"] to schedule in nodeManJson
            schedule.update(fullMessage["params"]["schedule"])
            break
        #Update to file
        NODE_MAN.syncToJsonFile(fileName=NODE_MANAGER_FILE, profileManager=nodeManJson)
        #Send all schedule list to web client
        __sendAllScheduleList(controllerUid,topic) #Send all schedule list to web client
      
      #A4. Remove schedule
      if "control.schedule.remove" in fullMessage["method"]:
        controllerUid = fullMessage["params"]["controllerUid"]
        print("\n\n\x1b[48;5;18m\x1b[38;5;3mGet request \x1b[48;5;1m\"control.schedule.remove\"\x1b[48;5;18m\x1b[38;5;3m from Socket for Controller: "+str(controllerUid)+"\x1b[0m")
        __checkExistProfile(controllerUid) #Check controllerUid exist in nodeManJson or not. If not, create new profile.
        #Send all schedule list to web client
        print("Remove schedule to controllerUid: "+str(fullMessage))
        for schedule in nodeManJson["NODE_"+controllerUid]["scheduleList"]:
          if int(schedule["scheduleUid"]) == int(fullMessage["params"]["scheduleUid"]):
            #Update fullMessage["params"]["schedule"] to schedule in nodeManJson
            nodeManJson["NODE_"+controllerUid]["scheduleList"].remove(schedule)
            break
        #Update to file
        NODE_MAN.syncToJsonFile(fileName=NODE_MANAGER_FILE, profileManager=nodeManJson)
        #Send all schedule list to web client
        __sendAllScheduleList(controllerUid,topic) #Send all schedule list to web client
      
      
      
      
      
      
      
      #### C. FROM GATEWAY ####
      #C1. Gateway update controller status as MANUAL ON
      
      #C2. Gateway update controller status as MANUAL OFF
      
      #C3. Gateway update controller status as AUTO - Control AUTO_ON/OFF base on schedule
      

      
#      and "problem.get" in fullMessage["method"]:
#      print("\nGet request SCAN_PROBLEM from Socket for HostGroup: "+fullMessage["params"]["hostgroupName"])
#      problemResult = getHostGroupProblem(hostgroupName=fullMessage["params"]["hostgroupName"])
#      if problemResult == False:
#        print("ERROR: Cannot get problem from Zabbix")
#        return False
#      else:
#        # pprint.pprint(problemResult)
#        topic=fullMessage["params"]["topic"]
#        fullMessage={
#          "uid": str(MQTT_CLIENT_ID),
#          "message":{
#            "method": "problem.update",
#            "params": problemResult
#          }
#        }
#        print("Publish SCAN_PROBLEM reuslt to Topic "+str(topic)+" with message:" + str(fullMessage))
#        MQTT.publish(str(topic), str(fullMessage))
      
  except Exception as e:
    print("ERROR: "+str(e))
    pass
        
def __checkExistProfile(controllerUid=""):
  if "NODE_"+controllerUid in nodeManJson:
    pass
  else:
    nodeManJson["NODE_"+controllerUid] = copy.deepcopy(controllerStr)
    #Update controllerUid
    nodeManJson["NODE_"+controllerUid]["info"]["controllerUid"] = controllerUid
    print("Create new profile for controllerUid: "+str(controllerUid))
    #Update to file
    NODE_MAN.syncToJsonFile(fileName=NODE_MANAGER_FILE, profileManager=nodeManJson)

def __sendAllScheduleList(controllerUid="", topic=""):
  messageContent = nodeManJson["NODE_"+controllerUid]["scheduleList"]
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