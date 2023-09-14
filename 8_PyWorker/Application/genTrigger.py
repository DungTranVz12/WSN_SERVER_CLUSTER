import __init
from time import sleep
# from Conf.loggingSetup import *
from pprint import *
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX
import time
############ IMPORT PARAMETER ############
import sys,os
if os.path.exists("/0_SHARE/myConfiguration.py"): #Mapped from host to container
  MAIN_WORKDIR = sys.path[0]
  os.system("cp /0_SHARE/myConfiguration.py "+MAIN_WORKDIR+"/cloneMyConfig.py")
  from cloneMyConfig import *
else:
  from Application.parameter import *
##########################################

################## TESTING #######################
ZABBIX_SERVER   = 'wsnCluster_zabbix-server-agent'
ZABBIX_WEB_IP   = 'wsnCluster_zabbix-web-nginx-mysql'
ZABBIX_WEB_PORT = '8080'
ZABBIX_PORT     = 10051
ZABBIX_USER     = 'Admin'
ZABBIX_PASS     = 'zabbix'
ZABBIX_URL      = 'http://'+ZABBIX_WEB_IP+':'+ZABBIX_WEB_PORT
gatewayName     = "01C821_GATEWAY_NODE"
devTrigCode     = "01C821.DEV_TRIG_CODE"
# hostGroupName   = "SeasideConsulting_GW01C821" 
# hostName        = "01C821_GATEWAY_NODE"
# itemName        = "DEV_TRIG_CODE"
# itemUID         = "01C821.DEV_TRIG_CODE"

zabbix = ZABBIX(ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_USER, ZABBIX_PASS,ZABBIX_URL,ZABBIX_MYSQL_UPLOAD=False)
# zabbix.createHostgroup(hostGroupName)
# #3. Tạo Host
# zabbix.createHost(hostGroupName, hostName)
# #4. Tạo Item
# zabbix.createItem(hostName,itemUID,itemName)

###################################################################
# LOW BATTERY TRIGGER                                             #
###################################################################
# ##### TEMP NODE: 1 #####
hostName        = "436730_NODE"
itemUID         = "01C821.436730.INSEN.02.1"
zabbix.updateItemValue(hostName,itemUID,100);
# zabbix.updateItemValue(hostName,itemUID,10) ;
# zabbix.updateItemValue(hostName,itemUID,100);

# ##### TEMP NODE: 2 #####
# hostName        = "C8DB2C_NODE"
# itemUID         = "01C821.C8DB2C.INSEN.02.1"
# zabbix.updateItemValue(hostName,itemUID,100);
# zabbix.updateItemValue(hostName,itemUID,10) ;
# zabbix.updateItemValue(hostName,itemUID,100);

# ##### TEMP NODE: 3 #####
# hostName        = "436774_NODE"
# itemUID         = "01C821.436774.INSEN.02.1"
# zabbix.updateItemValue(hostName,itemUID,100);
# zabbix.updateItemValue(hostName,itemUID,10) ;
# zabbix.updateItemValue(hostName,itemUID,100);

# ##### TEMP NODE: 4 #####
# hostName        = "436874_NODE"
# itemUID         = "01C821.436874.INSEN.02.1"
# zabbix.updateItemValue(hostName,itemUID,100);
# zabbix.updateItemValue(hostName,itemUID,10) ;
# zabbix.updateItemValue(hostName,itemUID,100);

# ##### SENSOR NODE: 1 - Low Internal Battery => Replace #####
# hostName        = "557E88_NODE"
# itemUID         = "01C821.557E88.INSEN.03.1"
# zabbix.updateItemValue(hostName,itemUID,1)
# zabbix.updateItemValue(hostName,itemUID,1)
# zabbix.updateItemValue(hostName,itemUID,1)
# zabbix.updateItemValue(hostName,itemUID,100)
# zabbix.updateItemValue(hostName,itemUID,100)
# zabbix.updateItemValue(hostName,itemUID,100)

# ##### SENSOR NODE: 2 - Low Internal Battery => Replace #####
# hostName        = "557D3C_NODE"
# itemUID         = "01C821.557D3C.INSEN.03.1"
# zabbix.updateItemValue(hostName,itemUID,1)
# zabbix.updateItemValue(hostName,itemUID,1)
# zabbix.updateItemValue(hostName,itemUID,1)
# zabbix.updateItemValue(hostName,itemUID,100)
# zabbix.updateItemValue(hostName,itemUID,100)
# zabbix.updateItemValue(hostName,itemUID,100)

###################################################################
# NO DATA TRIGGER                                                 #
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
# triggerId       = 23004
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)

#############################################################
# # # ##### TEMP NODE: 1 - Node no data #####
# triggerId       = 22993
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# # # ##### TEMP NODE: 2 - Node no data #####
# triggerId       = 22996
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# # # ##### TEMP NODE: 3 - Node no data #####
# triggerId       = 22994
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# # # ##### TEMP NODE: 4 - Node no data #####
# triggerId       = 22995
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)

#############################################################
# # # ##### SENSOR NODE: 1 - Node no data #####
# triggerId       = 23005
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# sleep(1)
# # ##### SENSOR NODE: 1 - DO no data #####
# triggerId       = 22998
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger
# # ##### SENSOR NODE: 1 - pH no data #####
# triggerId       = 22997
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger
# # ##### SENSOR NODE: 1 - Weather no data #####
# triggerId       = 22999
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger

#############################################################
# # # ##### SENSOR NODE: 2 - Node no data #####
# triggerId       = 23006
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId)
# zabbix.updateItemValue(gatewayName,devTrigCode,0)
# # ##### SENSOR NODE: 2 - DO no data #####
# triggerId       = 23001
# zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
# zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger
# # ##### SENSOR NODE: 2 - pH no data #####
triggerId       = 23002
zabbix.updateItemValue(gatewayName,devTrigCode,triggerId) #Trigger
zabbix.updateItemValue(gatewayName,devTrigCode,0)         #Clear Trigger

###################################################################
# THRESHOLD TRIGGER                                               #
###################################################################



