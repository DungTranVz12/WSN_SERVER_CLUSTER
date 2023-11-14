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
import time

#########################################################################################
# C. ZABBIX PART
#########################################################################################
zabbix = ZABBIX_LIB(ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_USER, ZABBIX_PASS, ZABBIX_URL,ZABBIX_MYSQL_UPLOAD=True)

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
    "uid": "Zabbix_Agent_11052",
    "message": {
      "method": "mail.send",
      "params": {
        "sendTo": "tran.dung@cmengineering.com.vn ",
        "subject": "[Zabbix Warning] PROBLEM: 436730_TEMP_NODE_1 - Low Battery",
        "body": {
          "MAIL.TEMPLATE":"Temp_01",
          "DATE":"2023.09.01",
          "TIME":"22:49:20",
          "EVENT.ID":"4175",
          "EVENT.NAME":"Low Battery",
          "EVENT.SEVERITY":"Warning",
          "EVENT.STATUS":"PROBLEM",
          "TRIGGER.HOSTGROUP.NAME":"SeasideConsulting_GW01C821",
          "HOST.ID":"10596",
          "HOST.NAME":"436730_TEMP_NODE_1",
          "ITEM.ID":"44412",
          "ITEM.NAME":"INSEN.02.1 - Internal battery percent",
          "ITEM.KEY":"01C821.436730.INSEN.02.1",
          "ITEM.LASTVALUE":"10 %",
          "ITEM.VALUE":"10 %",
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
      sendTo = str(params["sendTo"]).strip()
      subject = str(params["subject"]).strip()
      mailTemplate = str(params["body"]["MAIL.TEMPLATE"]).strip()
      date = str(params["body"]["DATE"]).strip()
      time = str(params["body"]["TIME"]).strip()
      eventId = str(params["body"]["EVENT.ID"]).strip()
      eventName = str(params["body"]["EVENT.NAME"]).strip()
      eventSeverity = str(params["body"]["EVENT.SEVERITY"]).strip()
      eventStatus = str(params["body"]["EVENT.STATUS"]).strip()
      hostGroupName = str(params["body"]["TRIGGER.HOSTGROUP.NAME"]).strip()
      hostName = str(params["body"]["HOST.NAME"]).strip()
      hostId = str(params["body"]["HOST.ID"]).strip()
      itemId = str(params["body"]["ITEM.ID"]).strip()
      itemName = str(params["body"]["ITEM.NAME"]).strip()
      itemKey = str(params["body"]["ITEM.KEY"]).strip()
      itemLastValue = str(params["body"]["ITEM.LASTVALUE"]).strip()
      itemValue = str(params["body"]["ITEM.VALUE"]).strip()
      itemValueType = str(params["body"]["ITEM.VALUETYPE"]).strip()
      
      #Convert sendTo to list
      SIB_SEND_TO = list()
      sendList = sendTo.split(",")
      for sendPerson in sendList:
         SIB_SEND_TO.append({"email":sendPerson})
      
      ###########################################################
      #2. Prepare mail content                                  #
      ###########################################################
      #2.1 Low Battery Template
      if mailTemplate == "Temp_01" or mailTemplate == "Temp_01_LowBattery": #Low Battery Template
        #2.1 load template to content
        with open(MAIN_WORKDIR+"/Application/MailTemplate/Temp_01_LowBattery.html", "r") as f:
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
        try:
          SIB.sendMail(mailConfig)
        except:
          SIB.sendMail(mailConfig)
        print("====> send mail success!")

      #2.2 No Data Template
      if mailTemplate == "Temp_02" or mailTemplate == "Temp_02_NoData": #No Data Template
        #2.1 load template to content
        with open(MAIN_WORKDIR+"/Application/MailTemplate/Temp_02_NoData.html", "r") as f:
          content = f.read()
          
        #2.2 Get Chart
        noDataKey = itemKey
        try:
          noDataKeyParams = zabbix.getItemParamByItemKey(noDataKey)
          noDataKeyId = noDataKeyParams["itemid"]
        except Exception as e:
          print("ERROR: "+str(e))
          noDataKeyId = "N/A"
        noDataChartB64,noDataChartLink = downloadBase64ZabbixChart(date,time,noDataKeyId)
        
        #2.3 Replace content
        content = content.replace("{{NO_DATA_GRAPH}}", noDataChartB64)
        content = content.replace("{{NO_DATA_GRAPH_LINK}}", noDataChartLink)

        #2.4 SendMail
        mailConfig.to = SIB_SEND_TO
        mailConfig.subject = subject
        mailConfig.content_mode = class_contentMode.HTML_CONTENT
        mailConfig.html_content = content
        mailConfig.attachment = [{'content':noDataChartB64, 'name':'noDataGraph.png'}]
        try:
          SIB.sendMail(mailConfig)
        except:
          SIB.sendMail(mailConfig)
        print("====> send mail success!")

      #2.3 No Data Recovery Template
      if mailTemplate == "Temp_03" or mailTemplate == "Temp_03_NoDataRecovery": #No Data Recovery Template
        #2.1 load template to content
        with open(MAIN_WORKDIR+"/Application/MailTemplate/Temp_03_NoDataRecovery.html", "r") as f:
          content = f.read()
          
        #2.2 Get Chart
        noDataKey = itemKey
        try:
          noDataKeyParams = zabbix.getItemParamByItemKey(noDataKey)
          noDataKeyId = noDataKeyParams["itemid"]
        except Exception as e:
          print("ERROR: "+str(e))
          noDataKeyId = "N/A"
        noDataChartB64,noDataChartLink = downloadBase64ZabbixChart(date,time,noDataKeyId)
        
        #2.3 Replace content
        content = content.replace("{{NO_DATA_GRAPH}}", noDataChartB64)
        content = content.replace("{{NO_DATA_GRAPH_LINK}}", noDataChartLink)

        #2.4 SendMail
        mailConfig.to = SIB_SEND_TO
        mailConfig.subject = subject
        mailConfig.content_mode = class_contentMode.HTML_CONTENT
        mailConfig.html_content = content
        mailConfig.attachment = [{'content':noDataChartB64, 'name':'noDataGraph.png'}]
        try:
          SIB.sendMail(mailConfig)
        except:
          SIB.sendMail(mailConfig)
        print("====> send mail success!")
        
      #2.4 Over Threshold Template
      if mailTemplate == "Temp_04" or mailTemplate == "Temp_04_OverThreshold": #Over Threshold Template
        #2.1 load template to content
        with open(MAIN_WORKDIR+"/Application/MailTemplate/Temp_04_OverThreshold.html", "r") as f:
          content = f.read()
          
        #2.2 Get Chart
        noDataKey = itemKey
        try:
          noDataKeyParams = zabbix.getItemParamByItemKey(noDataKey)
          noDataKeyId = noDataKeyParams["itemid"]
        except Exception as e:
          print("ERROR: "+str(e))
          noDataKeyId = "N/A"
        noDataChartB64,noDataChartLink = downloadBase64ZabbixChart(date,time,noDataKeyId)
        
        #2.3 Replace content
        content = content.replace("{{NO_DATA_GRAPH}}", noDataChartB64)
        content = content.replace("{{NO_DATA_GRAPH_LINK}}", noDataChartLink)

        #2.4 SendMail
        mailConfig.to = SIB_SEND_TO
        mailConfig.subject = subject
        mailConfig.content_mode = class_contentMode.HTML_CONTENT
        mailConfig.html_content = content
        mailConfig.attachment = [{'content':noDataChartB64, 'name':'noDataGraph.png'}]
        try:
          SIB.sendMail(mailConfig)
        except:
          SIB.sendMail(mailConfig)
        print("====> send mail success!")
        
      #2.5 Under Threshold Template
      if mailTemplate == "Temp_05" or mailTemplate == "Temp_05_UnderThreshold": #Under Threshold Template
        #2.1 load template to content
        with open(MAIN_WORKDIR+"/Application/MailTemplate/Temp_05_UnderThreshold.html", "r") as f:
          content = f.read()
          
        #2.2 Get Chart
        noDataKey = itemKey
        try:
          noDataKeyParams = zabbix.getItemParamByItemKey(noDataKey)
          noDataKeyId = noDataKeyParams["itemid"]
        except Exception as e:
          print("ERROR: "+str(e))
          noDataKeyId = "N/A"
        noDataChartB64,noDataChartLink = downloadBase64ZabbixChart(date,time,noDataKeyId)
        
        #2.3 Replace content
        content = content.replace("{{NO_DATA_GRAPH}}", noDataChartB64)
        content = content.replace("{{NO_DATA_GRAPH_LINK}}", noDataChartLink)

        #2.4 SendMail
        mailConfig.to = SIB_SEND_TO
        mailConfig.subject = subject
        mailConfig.content_mode = class_contentMode.HTML_CONTENT
        mailConfig.html_content = content
        mailConfig.attachment = [{'content':noDataChartB64, 'name':'noDataGraph.png'}]
        try:
          SIB.sendMail(mailConfig)
        except:
          SIB.sendMail(mailConfig)
        print("====> send mail success!")
        
      #2.7 Replace Battery Template
      if mailTemplate == "Temp_07" or mailTemplate == "Temp_07_ReplaceBattery": #Repace Battery Template
        #2.1 load template to content
        with open(MAIN_WORKDIR+"/Application/MailTemplate/Temp_07_ReplaceBattery.html", "r") as f:
          content = f.read()
          
        #2.2 Get Chart
        battVoltageKey = itemKey.rsplit(".",1)[0] + ".1" #Ex: 01C821.557E88.INSEN.03.1 - "INSEN.03.1 - 3.7 Internal battery voltage"
        try:
          battVoltageValueParams = zabbix.getItemParamByItemKey(battVoltageKey)
          battVoltageValue = battVoltageValueParams["lastvalue"]
          battVoltageId = battVoltageValueParams["itemid"]
        except Exception as e:
          print("ERROR: "+str(e))
          battVoltageValue = "N/A"
          battVoltageId = "N/A"
        battVoltageChartB64,battVoltageChartLink = downloadBase64ZabbixChart(date,time,battVoltageId)
        
        #2.3 Replace content
        content = content.replace("{{DEVICE_NAME}}" , hostName)
        content = content.replace("{{BATT_VOLTAGE}}", battVoltageValue)
        content = content.replace("{{BATT_VOLTAGE_GRAPH}}", battVoltageChartB64)
        content = content.replace("{{BATT_VOLTAGE_GRAPH_LINK}}", battVoltageChartLink)

        #2.4 SendMail
        mailConfig.to = SIB_SEND_TO
        mailConfig.subject = subject
        mailConfig.content_mode = class_contentMode.HTML_CONTENT
        mailConfig.html_content = content
        mailConfig.attachment = [{'content':battVoltageChartB64, 'name':'BatteryVoltage.png'}]
        try:
          SIB.sendMail(mailConfig)
        except:
          SIB.sendMail(mailConfig)
        print("====> send mail success!")


  except Exception as e:
    print("ERROR: "+str(e))
    pass
      

# MQTT.subscribe("WSN_GW_01C823.WEB.TEST")
MQTT.subscribe("ZABBIX_AGENT_PUBLISH")
MQTT.msgRcvFilter = subcribeFilter
threading.Thread(target=MQTT.listen).start()


##################################################################################################
