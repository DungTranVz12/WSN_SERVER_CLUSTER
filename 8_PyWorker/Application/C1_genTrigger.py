import __init
from time import sleep
# from Conf.loggingSetup import *
from pprint import *
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX
import time
import sys,os
devPcName = os.uname()[1]
############ IMPORT PARAMETER ############
if devPcName == "lotushp1":
  if os.path.exists("/root/myConfig/myConfigWSN.py"): #Mapped from host to container
    MAIN_WORKDIR = sys.path[0]
    os.system("cp /root/myConfig/myConfigWSN.py "+MAIN_WORKDIR+"/cloneMyConfig.py")
    from cloneMyConfig import *
  else:
    from Application.parameter import *
else:
  if os.path.exists("/myConfig/myConfigWSN.py"): #Mapped from host to container
    MAIN_WORKDIR = sys.path[0]
    os.system("cp /myConfig/myConfigWSN.py "+MAIN_WORKDIR+"/cloneMyConfig.py")
    from cloneMyConfig import *
  else:
    from Application.parameter import *
##########################################

################## TESTING #######################
#print dev PC Name

if devPcName == "lotushp1":
  print("Running on LotusHP1")
  ZABBIX_SERVER   = 'lotus1104.synology.me'
  ZABBIX_WEB_IP   = 'lotus1104.synology.me'
  ZABBIX_WEB_PORT = '10002'
  ZABBIX_PORT     = 10001
  ZABBIX_USER     = 'Admin'
  ZABBIX_PASS     = 'zabbix'
  ZABBIX_URL      = 'http://'+ZABBIX_WEB_IP+':'+ZABBIX_WEB_PORT
else:
  print("Running on Docker")
  ZABBIX_SERVER   = 'wsnCluster_zabbix-server-agent'
  ZABBIX_WEB_IP   = 'wsnCluster_zabbix-web-nginx-mysql'
  ZABBIX_WEB_PORT = '8080'
  ZABBIX_PORT     = 10051
  ZABBIX_USER     = 'Admin'
  ZABBIX_PASS     = 'zabbix'
  ZABBIX_URL      = 'http://'+ZABBIX_WEB_IP+':'+ZABBIX_WEB_PORT
gatewayName       = "01C821_GATEWAY_NODE"
devTrigCode       = "01C821.DEV_TRIG_CODE"

zabbix = ZABBIX(ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_USER, ZABBIX_PASS,ZABBIX_URL,ZABBIX_MYSQL_UPLOAD=False)





###################################################################
###################################################################
###################################################################
# 0. TEST ZABBIX CONNECTION                                       #
###################################################################
###################################################################
###################################################################
# hostGroupName     = "SeasideConsulting_GW01C821" 
# hostName          = "01C821_GATEWAY_NODE"
# itemName          = "TEST"
# itemUID           = "01C821.TEST"

# zabbix.createHostgroup(hostGroupName)
# #3. Tạo Host
# zabbix.createHost(hostGroupName, hostName)
# #4. Tạo Item
# zabbix.createItem(hostName,itemUID,itemName)
# #5. Update Item Value
# zabbix.updateItemValue(hostName,itemUID,0)
# zabbix.updateItemValue(hostName,itemUID,10)
# zabbix.updateItemValue(hostName,itemUID,20)
# zabbix.updateItemValue(hostName,itemUID,30)
# exit(0)





###################################################################
###################################################################
###################################################################
# 1. LOW BATTERY TRIGGER                                          #
###################################################################
###################################################################
###################################################################
# ##### TEMP NODE: 1 #####
# hostName        = "436730_NODE"
# itemUID         = "01C821.436730.INSEN.02.1"
# zabbix.updateItemValue(hostName,itemUID,100)  #Reset
# zabbix.updateItemValue(hostName,itemUID,25)   #First lower than Threshold  (<=30)
# zabbix.updateItemValue(hostName,itemUID,20)   #Second lower than Threshold (<=30)
# zabbix.updateItemValue(hostName,itemUID,15)   #Third lower than Threshold  (<=30)
# zabbix.updateItemValue(hostName,itemUID,10)   #Fourth lower than Threshold (<=30)
# sleep(5) # Wait for 3s to send mail
# zabbix.updateItemValue(hostName,itemUID,100)  #First Recovered
# zabbix.updateItemValue(hostName,itemUID,100)  #Second Recovered
# zabbix.updateItemValue(hostName,itemUID,100)  #Third Recovered

# ##### TEMP NODE: 2 #####
# hostName        = "C8DB2C_NODE"
# itemUID         = "01C821.C8DB2C.INSEN.02.1"
# zabbix.updateItemValue(hostName,itemUID,100)  #Reset
# zabbix.updateItemValue(hostName,itemUID,25)   #First lower than Threshold  (<=30)
# zabbix.updateItemValue(hostName,itemUID,20)   #Second lower than Threshold (<=30)
# zabbix.updateItemValue(hostName,itemUID,15)   #Third lower than Threshold  (<=30)
# zabbix.updateItemValue(hostName,itemUID,10)   #Fourth lower than Threshold (<=30)
# sleep(5) # Wait for 3s to send mail
# zabbix.updateItemValue(hostName,itemUID,100)  #First Recovered
# zabbix.updateItemValue(hostName,itemUID,100)  #Second Recovered
# zabbix.updateItemValue(hostName,itemUID,100)  #Third Recovered

# ##### TEMP NODE: 3 #####
# hostName        = "436774_NODE"
# itemUID         = "01C821.436774.INSEN.02.1"
# zabbix.updateItemValue(hostName,itemUID,100)  #Reset
# zabbix.updateItemValue(hostName,itemUID,25)   #First lower than Threshold  (<=30)
# zabbix.updateItemValue(hostName,itemUID,20)   #Second lower than Threshold (<=30)
# zabbix.updateItemValue(hostName,itemUID,15)   #Third lower than Threshold  (<=30)
# zabbix.updateItemValue(hostName,itemUID,10)   #Fourth lower than Threshold (<=30)
# sleep(5) # Wait for 3s to send mail
# zabbix.updateItemValue(hostName,itemUID,100)  #First Recovered
# zabbix.updateItemValue(hostName,itemUID,100)  #Second Recovered
# zabbix.updateItemValue(hostName,itemUID,100)  #Third Recovered

# ##### TEMP NODE: 4 #####
# hostName        = "436874_NODE"
# itemUID         = "01C821.436874.INSEN.02.1"
# zabbix.updateItemValue(hostName,itemUID,100)  #Reset
# zabbix.updateItemValue(hostName,itemUID,25)   #First lower than Threshold  (<=30)
# zabbix.updateItemValue(hostName,itemUID,20)   #Second lower than Threshold (<=30)
# zabbix.updateItemValue(hostName,itemUID,15)   #Third lower than Threshold  (<=30)
# zabbix.updateItemValue(hostName,itemUID,10)   #Fourth lower than Threshold (<=30)
# sleep(5) # Wait for 3s to send mail
# zabbix.updateItemValue(hostName,itemUID,100)  #First Recovered
# zabbix.updateItemValue(hostName,itemUID,100)  #Second Recovered
# zabbix.updateItemValue(hostName,itemUID,100)  #Third Recovered

# ##### SENSOR NODE: 1 - Low Internal Battery => Replace #####
# hostName        = "557E88_NODE"
# itemUID         = "01C821.557E88.INSEN.03.1"
# zabbix.updateItemValue(hostName,itemUID,4.25)  #Reset
# zabbix.updateItemValue(hostName,itemUID,3.0)   #First lower than Threshold  (<=3.5V)
# zabbix.updateItemValue(hostName,itemUID,2.9)   #Second lower than Threshold (<=3.5V)
# zabbix.updateItemValue(hostName,itemUID,2.8)   #Third lower than Threshold  (<=3.5V)
# sleep(5) # Wait for 3s to send mail
# zabbix.updateItemValue(hostName,itemUID,4.25)  #First Recovered
# zabbix.updateItemValue(hostName,itemUID,4.25)  #Second Recovered
# zabbix.updateItemValue(hostName,itemUID,4.25)  #Third Recovered

# ##### SENSOR NODE: 2 - Low Internal Battery => Replace #####
# hostName        = "557D3C_NODE"
# itemUID         = "01C821.557D3C.INSEN.03.1"
# zabbix.updateItemValue(hostName,itemUID,4.25)  #Reset
# zabbix.updateItemValue(hostName,itemUID,3.0)   #First lower than Threshold  (<=3.5V)
# zabbix.updateItemValue(hostName,itemUID,2.9)   #Second lower than Threshold (<=3.5V)
# zabbix.updateItemValue(hostName,itemUID,2.8)   #Third lower than Threshold  (<=3.5V)
# sleep(5)
# zabbix.updateItemValue(hostName,itemUID,4.25)  #First Recovered
# zabbix.updateItemValue(hostName,itemUID,4.25)  #Second Recovered
# zabbix.updateItemValue(hostName,itemUID,4.25)  #Third Recovered





###################################################################
###################################################################
###################################################################
# 2. NO DATA TRIGGER                                              #
###################################################################
###################################################################
###################################################################
# Clear No Data status
zabbix.updateItemValue("436730_NODE","01C821.436730.CH0.04.0",100)                 #Temp Node 1
zabbix.updateItemValue("C8DB2C_NODE","01C821.C8DB2C.CH0.04.0",100)                 #Temp Node 2
zabbix.updateItemValue("436774_NODE","01C821.436774.CH0.04.0",100)                 #Temp Node 3
zabbix.updateItemValue("436874_NODE","01C821.436874.CH0.04.0",100)                 #Temp Node 4
zabbix.updateItemValue("01C821_GATEWAY_NODE","01C821.01C821_GATEWAY.CPU_TEMP",50)  #Gateway
zabbix.updateItemValue("557E88_NODE","01C821.557E88.INSEN.03.0",12)                #Sensor Node 1
zabbix.updateItemValue("557E88_NODE","01C821.557E88.CH0.06.0",7)                   #Sensor Node 1 - pH
zabbix.updateItemValue("557E88_NODE","01C821.557E88.CH1.02.0",7)                   #Sensor Node 1 - DO
zabbix.updateItemValue("557E88_NODE","01C821.557E88.CH2.03.0",27)                  #Sensor Node 1 - Weather
zabbix.updateItemValue("557D3C_NODE","01C821.557D3C.INSEN.03.0",12)                #Sensor Node 2
zabbix.updateItemValue("557D3C_NODE","01C821.557D3C.CH0.06.0",7)                   #Sensor Node 2 - pH
zabbix.updateItemValue("557D3C_NODE","01C821.557D3C.CH1.02.0",7)                   #Sensor Node 2 - DO

#############################################################
# # # ##### GATEWAY - No data #####
# triggerId       = 22992
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)

#############################################################
# # # ##### TEMP NODE: 1 - Node no data #####
# triggerId       = 22997
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# # # ##### TEMP NODE: 2 - Node no data #####
# triggerId       = 23000
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# # # ##### TEMP NODE: 3 - Node no data #####
# triggerId       = 22998
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# # # ##### TEMP NODE: 4 - Node no data #####
# triggerId       = 22999
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)

#############################################################
# # # ##### SENSOR NODE: 1 - Node no data #####
# triggerId       = 22996
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# sleep(1)
# # ##### SENSOR NODE: 1 - DO no data #####
# triggerId       = 22989
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger
# # ##### SENSOR NODE: 1 - pH no data #####
# triggerId       = 23002
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger
# # ##### SENSOR NODE: 1 - Weather no data #####
# triggerId       = 23003
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger

#############################################################
# # # ##### SENSOR NODE: 2 - Node no data #####
# triggerId       = 22995
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# # ##### SENSOR NODE: 2 - DO no data #####
# triggerId       = 22988
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger
# # ##### SENSOR NODE: 2 - pH no data #####
# triggerId       = 23001
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger





###################################################################
###################################################################
###################################################################
# 3. THRESHOLD TRIGGER                                            #
###################################################################
###################################################################
###################################################################
# ##### SENSOR NODE: 1 - pH Sensor Over Threshold #####
# triggerId       = 23010
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# sleep(1)
# ##### SENSOR NODE: 1 - pH Sensor Under Threshold #####
# triggerId       = 23011
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger
# ##### SENSOR NODE: 1 - DO Sensor Under Threshold #####
# triggerId       = 23009
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger
# ##### SENSOR NODE: 1 - Water Temperature Over Threshold #####
# triggerId       = 23012
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# sleep(1)
# ##### SENSOR NODE: 1 - Water Temperature Over Threshold #####
# triggerId       = 23013
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger
#############################################################
# ##### SENSOR NODE: 2 - pH Sensor Over Threshold #####
# triggerId       = 23010
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# sleep(1)
# ##### SENSOR NODE: 2 - pH Sensor Under Threshold #####
# triggerId       = 23011
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger
# ##### SENSOR NODE: 2 - DO Sensor Under Threshold #####
# triggerId       = 23009
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger
# ##### SENSOR NODE: 2 - Water Temperature Over Threshold #####
# triggerId       = 23012
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# sleep(1)
# ##### SENSOR NODE: 2 - Water Temperature Over Threshold #####
# triggerId       = 23013
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger

#Print End Script with Red Ansi Color
print("\033[1;31;40m===== End SCRIPT =====\033[0m")