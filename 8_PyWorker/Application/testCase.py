import __init
from time import sleep
# from Conf.loggingSetup import *
from pprint import *
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX
from cloneMyConfig import *

################## TESTING #######################
ZABBIX_SERVER   = 'wsnCluster_zabbix-server-agent'
ZABBIX_WEB_IP   = 'wsnCluster_zabbix-web-nginx-mysql'
ZABBIX_WEB_PORT = '8080'
ZABBIX_PORT     = 10051
ZABBIX_USER     = 'Admin'
ZABBIX_PASS     = 'zabbix'
ZABBIX_URL      = 'http://'+ZABBIX_WEB_IP+':'+ZABBIX_WEB_PORT

hostGroupName   = "TestHostGroup" 
hostName        = "TestHost"
itemName        = "TestItem"
itemUID         = "TestUid.Test.1"

#1. Khởi tạo Zabbix
zabbix = ZABBIX(ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_USER, ZABBIX_PASS,ZABBIX_URL)
#2. Tạo Hostgroup
zabbix.createHostgroup(hostGroupName)
#3. Tạo Host
zabbix.createHost(hostGroupName, hostName)
#4. Tạo Item
zabbix.createItem(hostName,itemUID,itemName)

zabbix.updateItemValue (hostName, itemUID, value)







