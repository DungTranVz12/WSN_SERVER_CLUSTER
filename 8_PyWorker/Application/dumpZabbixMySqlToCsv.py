import __init
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX_LIB
import time,datetime
import pprint

########## USER CONFIG #######################
groupName = "AFOODS"
startTime = "2022/09/1 00:00:00"
endTime   = "2023/09/1 00:00:00"

MYSQL_HOST     = "wsn.com.vn"
MYSQL_DATABASE = "zabbixdb"
MYSQL_USER     = "jubei"
MYSQL_PASS     = "Shinghen123"
sql = MYSQL(MYSQL_HOST,MYSQL_USER,MYSQL_PASS,MYSQL_DATABASE)

ZABBIX_SERVER   = 'wsn.com.vn'
ZABBIX_PORT     = 10051
ZABBIX_USER     = 'Admin'
ZABBIX_PASS     = 'CMEV12345'
ZABBIX_URL      = 'http://'+ZABBIX_SERVER+'/zabbix/'
zabbix = ZABBIX_LIB(ZABBIX_SERVER, ZABBIX_PORT, ZABBIX_USER, ZABBIX_PASS, ZABBIX_URL,ZABBIX_MYSQL_UPLOAD=True)

###############################################
epochStartTime = int(time.mktime(time.strptime(startTime, "%Y/%m/%d %H:%M:%S")))
epochEndTime = int(time.mktime(time.strptime(endTime, "%Y/%m/%d %H:%M:%S")))

print("===== SCRIPT AUTO EXPORT ZABBIX DATA TO CSV FILE =====")
print("From: ",startTime," To: ",endTime)
print()

#1. Build host list
groupID = zabbix.getHostGroupID(groupName)
hostList = []
hostGetResult = zabbix.zabbix_api.do_request('host.get', {'groupids': [groupID]})["result"]
for host in hostGetResult:
  hostName = host["name"]
  # hostList.append(f'{"hostName":"{hostName}"}')
  hostList.append({"hostName":str(hostName),"hostId":str(host["hostid"])})
# pprint.pprint(hostList)

n=0
for host in hostList:
  #2. Build item list
  hostName = host["hostName"]
  hostId   = host["hostId"]
  itemList = []
  itemGetResult = zabbix.zabbix_api.do_request('item.get', {'hostids': [hostId]})["result"]
  for item in itemGetResult:
    # pprint.pprint(item)
    itemName = item["name"]
    itemKey  = item["key_"]
    itemUnit = item["units"]
    itemid   = item["itemid"]
    itemValueType = item["value_type"]
    itemList.append({"itemName":str(itemName),"itemKey":str(itemKey),"itemUnit":str(itemUnit),"itemid":str(itemid),"itemValueType":str(itemValueType)})
    # MAKE CSV FILE
    fileName = str(hostName+"_"+itemName).replace(" ","_").replace("-","_").replace("/","_").replace("(","_").replace(")","_").replace(".","_").replace(",","_").replace(":","_")+".csv"
    print(datetime.datetime.now().strftime("[🕔 %H:%M:%S]")+" "+fileName)
    with open(fileName, "w") as f:
      f.write('"DateTime","Value","Unit"\n')
      if itemValueType == "0":
        readData = sql.customSelect("SELECT clock,value FROM history WHERE itemid="+str(itemid)+" AND clock BETWEEN "+str(epochStartTime)+" AND "+str(epochEndTime)+" ORDER BY clock ASC")
      else:
        readData = sql.customSelect("SELECT clock,value FROM history_text WHERE itemid="+str(itemid)+" AND clock BETWEEN "+str(epochStartTime)+" AND "+str(epochEndTime)+" ORDER BY clock ASC")
      for row in readData:
        # print(row)
        clock = row["clock"]
        value = row["value"]
        if itemValueType != "0": #If value type is text
          value = value.decode("utf-8") #Convert value from byte (b'...') to string

        #Convert timestamp to datetime
        dateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(clock))
        f.write(f'"{dateTime}","{value}","{itemUnit}"\n') #Print to CSV format
    
    
  hostList[n]["itemList"] = itemList
  n+=1
# pprint.pprint(hostList)
