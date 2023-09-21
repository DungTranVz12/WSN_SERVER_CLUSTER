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
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX_LIB
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt
import threading
from Application.Others.downloadZabbixGraph import *
from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
from time import sleep

#########################################################################################
# C. ZABBIX PART
#########################################################################################
zabbix = ZABBIX_LIB(ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_USER, ZABBIX_PASS, ZABBIX_URL,ZABBIX_MYSQL_UPLOAD=True)
while True:
  print(">>> Update value to 10 <<<")
  # hostGroupName   = "SeasideConsulting_GW_TEST" 
  # hostName        = "TEMP_NODE_1"
  # itemName        = "INSEN.02.1 - Internal battery percent"
  # itemKey         = "INSEN.02.1"
  # #2. Tạo Hostgroup
  # zabbix.createHostgroup(hostGroupName)
  # #3. Tạo Host
  # zabbix.createHost(hostGroupName, hostName)
  # #4. Tạo Item
  # zabbix.createItem(hostName,itemKey,itemName)

  # problemHostQuerry = {
  #     "method": "host.get",
  #     "params": {
  #         "groupids": hostGroupId,
  #         "severities": [2, 5] # 0: not classified; 1: information; 2: warning; 3: average; 4: high; 5: disaster
  #     },
  #     "id": 1
  # }
  import pprint
  import time
  # result = zabbix.zabbix_api.do_request('host.get', {'filter': {'host': [hostName]}})
  while True:
    print(">>> Update value to 10 <<<")

    itemId  = zabbix.getItemID("436730_NODE","01C821.436730.INSEN.02.1")
    zabbix.updateItemValueMySqlOrSender(itemId,112,time.time())
    
    hostName = "436730_NODE"
    itemKey  = "01C821.436730.INSEN.02.1"
    zabbix.updateItemValue (hostName, itemKey, 100)

    hostName = "TestHost"
    itemKey  = "TestUid.Test.1"
    zabbix.updateItemValue (hostName, itemKey, 10)
    
    print()
    print()
    time.sleep(1)
  
  problemHostQuerry= {
    "jsonrpc": "2.0",
    "method": "item.update",
    "params": {
        "key_": "01C821.436730.INSEN.02.1",
        "lastvalue": "200"
    },
    "id": 1
  }
  problemHostResult = zabbix.zabbix_api.do_request(problemHostQuerry["method"], problemHostQuerry["params"])["result"]
  print(problemHostResult)


  hostName = "436730_TEMP_NODE_1"       # Seaside Consulting Temperature Node 1
  itemKey  = "01C821.436730.INSEN.02.1" # Seaside Consulting Battery Percent
  zabbix.updateItemValue (hostName, itemKey, 10)
  
  hostName = "TestHost"
  itemKey  = "TestUid.Test.1"
  zabbix.updateItemValue (hostName, itemKey, 10)
  sleep(2)

#########################################################################################
# B. MQTT PART
#########################################################################################
############################################################
# 1. CONNECT TO MQTT BROKER                                #
############################################################
MQTT = mqttClass(MQTT_BROKER_IP, MQTT_PORT, MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD)
def subcribeFilter(msg):
  '''
  {
    "uid": "Zabbix_Agent_22710",
    "message": {
      "method": "mail.send",
      "params": {
        "sendTo": "tran.dung@cmengineering.com.vn",
        "subject": "[Zabbix Warning] PROBLEM: OverThreshold",
        "body": {
          "MailTemplate":"Template_ABC",
          "DATE":"2023.08.29",
          "TIME":"23:28:41",
          "EVENT.ID":"7205",
          "EVENT.NAME":"OverThreshold",
          "EVENT.SEVERITY":"High",
          "EVENT.STATUS":"PROBLEM",
          "TRIGGER.HOSTGROUP.NAME":"TestHostGroup",
          "HOST.NAME":"TestHost",
          "HOST.ID":"10622",
          "ITEM.ID":"44665",
          "ITEM.NAME":"TestItem",
          "ITEM.KEY":"TestUid.Test.1",
          "ITEM.LASTVALUE":"30",
          "ITEM.VALUE":"40",
          "ITEM.VALUETYPE":"0"
       }
      }
    }
  }
  '''
  try:
    jsonData = eval(str(msg.payload.decode()))
    if "mail.send" == jsonData["message"]["method"]:  #METHOD = "mail.send"
      params = jsonData["message"]["params"]
      #1. META DATA
      sendTo = params["sendTo"]
      subject = params["subject"]
      mailTemplate = params["body"]["MAIL.TEMPLATE"]
      date = params["body"]["DATE"]
      time = params["body"]["TIME"]
      eventId = params["body"]["EVENT.ID"]
      eventName = params["body"]["EVENT.NAME"]
      eventSeverity = params["body"]["EVENT.SEVERITY"]
      eventStatus = params["body"]["EVENT.STATUS"]
      hostGroupName = params["body"]["TRIGGER.HOSTGROUP.NAME"]
      hostName = params["body"]["HOST.NAME"]
      hostId = params["body"]["HOST.ID"]
      itemId = params["body"]["ITEM.ID"]
      itemName = params["body"]["ITEM.NAME"]
      itemKey = params["body"]["ITEM.KEY"]
      itemLastValue = params["body"]["ITEM.LASTVALUE"]
      itemValue = params["body"]["ITEM.VALUE"]
      itemValueType = params["body"]["ITEM.VALUETYPE"]
      
      #Convert sendTo to list
      SIB_SEND_TO = list()
      sendList = sendTo.split(",")
      for sendPerson in sendList:
         SIB_SEND_TO.append({"email":sendPerson})
      
      #2. Prepare mail content
      if mailTemplate == "Temp_01":
        #2.1 load template to content
        with open(MAIN_WORKDIR+"/Application/MailTemplate/Temp_01.html", "r") as f:
          content = f.read()
          
        #2.2 Get Chart
        battPercentKey = itemKey.rsplit(".",1)[0] + ".1" #Ex: 01C821.436730.INSEN.02.1
        battVoltageKey = itemKey.rsplit(".",1)[0] + ".0" #Ex: 01C821.436730.INSEN.02.0
        try:
          battPercentParams = zabbix.getItemParamByItemKey(battPercentKey)
          battPercentValue = battPercentParams["lastvalue"]
          battPercentId = battPercentParams["itemid"]
          
          battVoltageValueParams = zabbix.getItemParamByItemKey(battVoltageKey)
          battVoltageValue = battVoltageValueParams["lastvalue"]
          battVoltageId = battVoltageValueParams["itemid"]
        except Exception as e:
          print("ERROR: "+str(e))
          battPercentValue = "N/A"
          battVoltageValue = "N/A"
          battPercentId = "N/A"
          battVoltageId = "N/A"
        battPercentChartB64,battPercentChartLink = downloadBase64ZabbixChart(date,time,battPercentId)
        battVoltageChartB64,battVoltageChartLink = downloadBase64ZabbixChart(date,time,battVoltageId)
        
        #2.3 Replace content
        content = content.replace("{{DEVICE_NAME}}" , hostName)
        content = content.replace("{{BATT_PERCENT}}", battPercentValue)
        content = content.replace("{{BATT_VOLTAGE}}", battVoltageValue)
        content = content.replace("{{BATT_PERCENT_GRAPH}}", battPercentChartB64)
        content = content.replace("{{BATT_VOLTAGE_GRAPH}}", battVoltageChartB64)
        content = content.replace("{{BATT_PERCENT_GRAPH_LINK}}", battPercentChartLink)
        content = content.replace("{{BATT_VOLTAGE_GRAPH_LINK}}", battVoltageChartLink)

        #2.4 SendMail
        mailConfig.to = SIB_SEND_TO
        mailConfig.subject = subject
        mailConfig.content_mode = class_contentMode.HTML_CONTENT
        mailConfig.html_content = content
        mailConfig.attachment = [{'content':battPercentChartB64, 'name':'BatteryPercent.png'},
                                 {'content':battVoltageChartB64, 'name':'BatteryVoltage.png'}]
        SIB.sendMail(mailConfig)
        pass
    
  except Exception as e:
    print("ERROR: "+str(e))
    pass
      

MQTT.subscribe("WSN_GW_01C823.WEB.TEST")
MQTT.subscribe("ZABBIX_AGENT_PUBLISH")
MQTT.msgRcvFilter = subcribeFilter
threading.Thread(target=MQTT.listen).start()


##################################################################################################
sleep(2)
print("===== TESTCASE GENERATION =====")
hostName = "436730_TEMP_NODE_1"       # Seaside Consulting Temperature Node 1
itemKey  = "01C821.436730.INSEN.02.1" # Seaside Consulting Battery Percent
zabbix.updateItemValue (hostName, itemKey, 10)
print("===== DONE =====")
