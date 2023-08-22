import __init
from time import sleep
from Conf.loggingSetup import *
from pprint import *
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX


################## TESTING #######################
zabbix_server   = '128.199.153.250'
zabbix_port     =  10051
zabbix_user     = 'admin'
zabbix_password = 'CMEV12345'

hostGroupName   = "GWUID_WSN_Gateway" 
hostName        = "NODEUID_Sensor_Node"
itemName        = "NODEUID_CH0"
itemUID         = "GWUID.NODEUID.CH0" # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.

#1. Khởi tạo Zabbix
ZABBIX().__init__(zabbix_server, zabbix_port, zabbix_user, zabbix_password)
#2. Tạo Hostgroup
ZABBIX().createHostgroup(hostGroupName)

#3. Tạo Host
ZABBIX().createHost(hostGroupName, hostName)
#4. Tạo Item
ZABBIX().createItem(hostName,itemUID,itemName)

#6. Lấy giá trị HostGroupID
hostGroupId = ZABBIX().getHostGroupID(hostGroupName)
print("hostGroupId: ", hostGroupId)
#7. Lấy giá trị HostID
hostId = ZABBIX().getHostID(hostName)
print("HostID: ",hostId)
#8. Lấy giá trị ItemID
itemId = ZABBIX().getItemID(hostName,itemName)
print("ItemID: ",itemId)

hostGroupName = ZABBIX().getHostGroupName(hostGroupId)
print("hostGroupName: ",hostGroupName)
#5. Cập nhật giá trị cho Item
#5.1 Lấy giá trị hostname trước khi cập nhật
hostName = ZABBIX().getHostName(hostId)
print("hostName: ",hostName)
ZABBIX().updateItemValue (hostName, itemUID, 360)
### RESULT ###
# ../Components/PIC/001.png


#9. Truy xuất toàn bộ parameter của Item 
itemParam1 = ZABBIX().getItemParam(hostName,itemName)
# pprint("ItemParam1: ",itemParam1)
#10. Cập nhật giá trị parameter cho Item
ZABBIX().updateItemParam(hostName,itemName,{"units": "bpm"})
#11. Truy xuất toàn bộ parameter của Item lần 2
itemParam2 = ZABBIX().getItemParam(hostName,itemName)
pprint(itemParam2)

# ZABBIX().renameHostgroup("73","ABCDEF123")


hostParam1 = ZABBIX().getHostParam(hostName)
pprint(hostParam1)




