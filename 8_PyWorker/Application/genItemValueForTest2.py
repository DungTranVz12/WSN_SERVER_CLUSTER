import __init
from time import sleep
# from Conf.loggingSetup import *
from pprint import *
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX
import time
############ IMPORT PARAMETER ############
import sys,os
if os.path.exists("/myConfigWSN.py"): #Mapped from host to container
  MAIN_WORKDIR = sys.path[0]
  os.system("cp /0_SHARE/myConfigWSN.py "+MAIN_WORKDIR+"/cloneMyConfig.py")
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

hostGroupName   = "SeasideConsulting_GW01C821" 
hostName        = "436730_NODE"
itemName        = "INSEN.02.1 - Internal battery percent"
itemUID         = "01C821.436730.INSEN.02.1"

#1. Khởi tạo Zabbix
zabbix = ZABBIX(ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_USER, ZABBIX_PASS,ZABBIX_URL,ZABBIX_MYSQL_UPLOAD=False)
#2. Tạo Hostgroup
zabbix.createHostgroup(hostGroupName)
#3. Tạo Host
zabbix.createHost(hostGroupName, hostName)
#4. Tạo Item
zabbix.createItem(hostName,itemUID,itemName)

#Update giá trị cho Item từ 0 đến 100 sau mỗi 1s.
#Buóc nhảy là 10
#Khi giá trị đạt 100 thì giảm dần xuống 0. Mỗi bước nhảy là 10
#Lăp lại quá trình trên
MAX_VALUE      = 100
MIN_VALUE      = 0
STEP_VALUE     = 10
STEP_DELAY_SEC = 0.5

print("\n=== START TEST ===")
while True:
  for i in range(MAX_VALUE,MIN_VALUE,-STEP_VALUE):
    print("Upload value: ", str(i))
    itemId  = zabbix.getItemID(hostName, itemUID)
    zabbix.updateItemValue(hostName, itemUID,i)
    sleep(STEP_DELAY_SEC)
  for i in range(MIN_VALUE,MAX_VALUE,STEP_VALUE):
    print("Upload value: ", str(i))
    itemId  = zabbix.getItemID(hostName, itemUID)
    zabbix.updateItemValue(hostName, itemUID,i)
    sleep(STEP_DELAY_SEC)

    



