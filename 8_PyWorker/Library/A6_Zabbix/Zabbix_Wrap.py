import __init
from time import sleep
from Conf.loggingSetup import *
from pyzabbix import ZabbixMetric, ZabbixSender
from pyzabbix.api import ZabbixAPI
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
import time

class zabbix_Wrapper:
  def __init__(self, zabbix_server = '128.199.153.250', zabbix_port = 10051 , zabbix_user = 'admin', zabbix_password = 'CMEV12345',zabbix_url="http://128.199.153.250/zabbix",
               mysqlHost="wsnCluster_zabbix-mysql-server",mySqlUser="zabbix",mySqlPass="zabbix_pwd",mySqlDatabase="zabbix",ZABBIX_MYSQL_UPLOAD=False):
    self.zabbix_server = zabbix_server
    self.zabbix_port = zabbix_port
    self.zabbix_user = zabbix_user
    self.zabbix_password = zabbix_password
    self.zabbix_api = ZabbixAPI(url=zabbix_url, user=self.zabbix_user, password=self.zabbix_password)
    self.zabbix_mysql_upload = ZABBIX_MYSQL_UPLOAD
    if self.zabbix_mysql_upload == True:
      self.zabbixMySql = MYSQL(mysqlHost,mySqlUser,mySqlPass,mySqlDatabase)
    
  def createHostgroup(self,zbx_hostgroup):
    '''
    - `name`: createHostgroup
    - `description`:  Tạo hostgroup trên Zabbix.
    - `parameters`:
      - `zbx_hostgroup`: Tên hostgroup.
    - `return`: None
    - `Example`:
        - createHostgroup('ABC_Customer')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    try:
        result = self.zabbix_api.do_request('hostgroup.get', {'search': {'name': [zbx_hostgroup]}})
        if [name['name'] for name in result['result']] == []:
            self.zabbix_api.hostgroup.create(name=zbx_hostgroup)
            logger.info(f'[Zabbix] Hostgroup created: {zbx_hostgroup} : {str(result)}')      # log hostgroup creation
    except Exception:
        logger.error('[Zabbix] Unable to request to server')

  def getHostGroupID (self,hostgroupName):
    '''
    - `name`: getHostGroupID
    - `description`:  Lấy ID của hostgroup.
    - `parameters`:
      - `hostgroupName`: Tên hostgroup.
    - `return`: ID của hostgroup.
    - `Example`:
      - getHostGroupID('ABC_Customer')
    '''
    try:
        result = self.zabbix_api.do_request('hostgroup.get', {'search': {'name': [hostgroupName]}})
        if [name['name'] for name in result['result']] == []:
            return False
        else:
            return [name['groupid'] for name in result['result']][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False

  def getHostGroupName(self,zbx_hostgroup_id):
    '''
    - `name`: getHostGroupName
    - `description`:  Lấy tên hostgroup.
    - `parameters`:
      - `zbx_hostgroup_id`: ID của hostgroup.
    - `return`: Tên hostgroup.
    - `Example`:
        - getHostGroupName('1')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    try:
        result = self.zabbix_api.do_request('hostgroup.get', {'search': {'groupid': [zbx_hostgroup_id]}})
        if [name['name'] for name in result['result']] == []:
            return False
        else:
            return [name['name'] for name in result['result']][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False
      
  def renameHostgroup(self,zbx_hostgroup_id,zbx_hostgroup_new_name):
    '''
    - `name`: createHostgrenameHostgrouproup
    - `description`:  Đặt lại tên cho Hostgroup.
    - `parameters`:
      - `zbx_hostgroup_id`: ID của hostgroup.
      - `zbx_hostgroup_new_name`: Tên mới của hostgroup.
    - `return`: None
    - `Example`:
        - renameHostgroup('1', 'ABC_Customer')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    try:
      self.zabbix_api.hostgroup.update(groupid=str(zbx_hostgroup_id),name=str(zbx_hostgroup_new_name))
      logger.info(f'[Zabbix] Hostgroup renamed: {zbx_hostgroup_new_name}')      # log hostgroup creation
    except Exception:
        logger.error('[Zabbix] Unable to request to server')

  def createHost(self,zbx_hostgroup, zbx_host):
    '''
    - `name`: createHost
    - `description`:  Tạo host trên Zabbix.
    - `parameters`:
      - `zbx_hostgroup`: Tên hostgroup.
      - `zbx_host`: Tên host.
    - `return`: None
    - `Example`:
        - createHost('ABC_Customer', 'DaLat_Tanung_GW0')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    try:
        result = self.zabbix_api.do_request('host.get', {'search':{'host':[zbx_host]}})
        if [host['host'] for host in result['result']] != []:
            return True
        else:
            result = self.zabbix_api.do_request('hostgroup.get', {'search': {'name': [zbx_hostgroup]}})
            if [name['name'] for name in result['result']] == []:
                # HostGroup doesn't exist
                return False
            else:
                groupId = [name['groupid'] for name in result['result']][0]
                self.zabbix_api.do_request('host.create', {'host': zbx_host, 'interfaces': [{'type': 1, 'main': 1, 'useip': 1, 'ip': '127.0.0.1', 'dns': '', 'port': self.zabbix_port}], 'groups': [{'groupid': groupId}]})
                logger.info(f'[Zabbix] Host created: {zbx_host}')
                return True
    except Exception:
        logger.error('[Zabbix] Unable to request to server')

  def getHostID (self,hostName):
    '''
    - `name`: getHostID
    - `description`:  Lấy ID của host.
    - `parameters`:
      - `hostName`: Tên host.
    - `return`: ID của host.
    - `Example`:
      - getHostID('DaLat_Tanung_GW0')
    '''
    try:
        result = self.zabbix_api.do_request('host.get', {'search': {'host': [hostName]}})
        if [host['host'] for host in result['result']] == []:
            return False
        else:
            return [host['hostid'] for host in result['result']][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False

  def getHostName (self,hostID):
    '''
    - `name`: getHostName
    - `description`:  Lấy tên host.
    - `parameters`:
      - `hostID`: ID của host.
    - `return`: Tên host.
    - `Example`:
      - getHostName('10050')
    '''
    try:
        result = self.zabbix_api.do_request('host.get', {'search': {'hostid': [hostID]}})
        if [host['hostid'] for host in result['result']] == []:
            return False
        else:
            return [host['host'] for host in result['result']][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False

  def createItem(self,zbx_host, zbx_item_UID, zbx_item_name):
    '''
    - `name`: createItem
    - `description`:  Tạo item trên Zabbix.
    - `parameters`:
      - `zbx_host`: Tên host.
      - `zbx_item_UID`: UID của item. VD: 201X0.1.2 # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.
      - `zbx_item_name`: Tên item.
    - `return`: None
    - `Example`:
        - createItem('DaLat_Tanung_GW0', '201X0.1.2', 'CH2')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    try:
        result = self.zabbix_api.do_request('item.get', {'host': zbx_host, 'search': {'key_':[zbx_item_UID]}})
        if [host['key_'] for host in result['result']] != []:
            return True
        else:
            result = self.zabbix_api.do_request('host.get', {'search':{'host':[zbx_host]}})
            if [host['host'] for host in result['result']] == []:
                # Host doesn't exist
                return False
            else:
                hostId = [item['hostid'] for item in result['result']][0]
                self.zabbix_api.do_request('item.create', {'hostid': hostId, 'value_type': '0','type': '2', 'name': zbx_item_name, 'key_': zbx_item_UID})
                logger.info(f'[Zabbix] Item created: {zbx_item_name}')
                return True
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False

  def getItemID (self,hostName,itemKey):
    '''
    - `name`: getItemID
    - `description`:  Lấy ID của item.
    - `parameters`:
      - `hostName`: Tên host.
      - `itemKey`: item key.
    - `return`: ID của item.
    - `Example`:
      - getItemID('DaLat_Tanung_GW0',"201X0.1.2")
    '''
    try:
        result = self.zabbix_api.do_request('item.get', {'host': hostName, 'search': {'key_': [itemKey]}})
        if [item['name'] for item in result['result']] == []:
            return False
        else:
            return [item['itemid'] for item in result['result']][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False
      
  def updateItemValue (self,zbx_host, zbx_item_UID, zbx_item_value,clockNs=None):
    '''
    - `name`: updateItemValue
    - `description`:  Tạo item trên Zabbix.
    - `parameters`:
      - `zbx_host`: Tên host.
      - `zbx_item_UID`: UID của item. VD: 201X0.1.2 # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.
      - `zbx_item_value`: Giá trị item.
      - `clockNs`: Thời gian clock và nano second trên bảng của Zabbix/histry của giá trị item. Nếu không có thì lấy thời gian hiện tại.
    - `return`: None
    - `Example`:
      - updateItemValue('DaLat_Tanung_GW0', '201X0.1.2', '250')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    if clockNs == None:
      metrics = [ZabbixMetric(zbx_host, zbx_item_UID, zbx_item_value)]
    else:
      metrics = [ZabbixMetric(zbx_host, zbx_item_UID, zbx_item_value,clock=clockNs)]
    ZabbixSender(zabbix_server=self.zabbix_server, zabbix_port=self.zabbix_port).send(metrics)
    
  def updateItemValueMySqlOrSender(self,itemId_MySql:int=123456, zbx_item_value=0,epochTimeStamp:float=None,hostName_zabbixSender:str=None,itemKey_zabbixSender:str=None):
    '''
    - `name`: updateItemValueMySqlOrSender
    - `description`:  Upload giá trị của item lên mysql trực tiếp (Nếu có cấu hình ZABBIX_MYSQL_UPLOAD = True) hoặc gửi giá trị của item lên Zabbix Server (Nếu có cấu hình ZABBIX_MYSQL_UPLOAD = False).
    - `parameters`:
      - `itemId_MySql`: UID của item (Key của item).
      - `zbx_item_value`: Giá trị item.
      - `epochTimeStamp`: Thời gian của giá trị item. Nếu không có thì lấy thời gian hiện tại.
      - `hostName`: Tên host. Nếu không có thì lấy thời tên host của itemId.
      - `itemKey`: Key của item. Nếu không có thì lấy key của itemId.
    - `return`: None
    - `Example`:
      - ZABBIX_MYSQL_UPLOAD = True
      - updateItemValueMySqlOrSender(123456, 250, time.time(), 'DaLat_Tanung_GW0', '201X0.1.2'
    '''
    # INSERT INTO `history` (`itemid`, `clock`, `value`, `ns`) VALUES ('44412', '1693560397', '40', '0');
    if self.zabbix_mysql_upload == True:
      try:
        print("Upload to Zabbix Server by MySQL")
        if epochTimeStamp == None: epochTimeStamp = time.time()
        print(epochTimeStamp)
        clock = int(epochTimeStamp)
        ns = int((epochTimeStamp - clock)* 1000000000)
        
        #Correct type of zbx_item_value
        if type(zbx_item_value) == str:
          zbx_item_value = f'"{zbx_item_value}"'
        elif type(zbx_item_value) == int:
          zbx_item_value = f'{zbx_item_value}'
        elif type(zbx_item_value) == float:
          zbx_item_value = f'{zbx_item_value}'
        else:
          zbx_item_value = f'"{zbx_item_value}"'
            
        #Insert to mysql
        columnString = 'itemid, clock, value, ns'
        valueString  = str(itemId_MySql)+','+str(clock)+','+str(zbx_item_value)+','+str(ns)
        print(valueString)
        self.zabbixMySql.insertRow("history", columnString, valueString)
      except Exception as e:
        print(e)
        logger.error('[Zabbix] Unable to request to server')
    else:
      try:
        print("Upload to Zabbix Server by ZabbixSender")
        self.updateItemValue(hostName_zabbixSender,itemKey_zabbixSender,zbx_item_value)
      except Exception as e:
        print(e)
        logger.error('[Zabbix] Unable to request to server')
      

  


  def getHostParam (self,hostName):
    '''
    - `name`: getHostParam
    - `description`:  Lấy các tham số của host.
    - `parameters`:
      - `hostName`: Tên host.
    - `return`: Các tham số của host.
    - `Example`:
      - getHostParam('DaLat_Tanung_GW0')
    '''
    try:
        result = self.zabbix_api.do_request('host.get', {'search': {'host': [hostName]}})
        if [host['host'] for host in result['result']] == []:
            return False
        else:
            return result['result'][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False
      
  def getItemParam (self,hostName,itemName):
    '''
    - `name`: getItemValue
    - `description`:  Lấy giá trị của item.
    - `parameters`:
      - `hostName`: Tên host.
      - `itemName`: Tên item.
    - `return`: Giá trị của item. Dạng dictionary.
    - `Example`:
      - getItemValue('DaLat_Tanung_GW0', "201X0.1.2")
    '''
    try:
        result = self.zabbix_api.do_request('item.get', {'host': hostName, 'search': {'name': [itemName]}})
        return result['result'][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False

  def getItemParamByItemKey (self,itemKey):
    '''
    - `name`: getItemParamByItemKey
    - `description`:  Lấy các thông số của item dựa vào itemKey.
    - `parameters`:
      - `itemKey`: Key của item.
    - `return`: Giá trị của item. Dạng dictionary.
    - `Example`:
      - getItemParamByItemKey("201X0.1.2")
    '''
    try:
        result = self.zabbix_api.do_request('item.get', {'search': {'key_': [itemKey]}})
        return result['result'][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False
      
  def updateItemParam (self,hostName,itemKey, updateParamDict={}):
    '''
    - `name`: updateItemParam
    - `description`: Cập nhật tham số của item.
    - `parameters`:
      - `hostName`: Tên host.
      - `itemKey`: Tên item key.
      - `updateParamDict`: Danh sách tham số cần cập nhật dạng dict.\\
         Ex: {"units": "bpm"}\\
         Danh sách item's parameter: https://www.zabbix.com/documentation/6.0/en/manual/api/reference/item/object
    - `return`: None
    - `Example`:
      - updateItemParam("DaLat_Tanung_GW0","201X0.1.2",{"units": "bpm"})
    '''
    try:
        itemId = self.getItemID(hostName,itemKey)
        updateDict = {'itemid': itemId}
        updateDict.update(updateParamDict)
        return self.zabbix_api.do_request('item.update',updateDict)
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False
      
  def checkGroupProblem (self,hostGroupId:int=0,zabbixServerIp:str=""):
    '''
    - `name`: checkItemProblem
    - `description`: Kiểm tra item có đang bị lỗi hay không.
    - `parameters`:
      - `hostName`: Tên host.
      - `itemName`: Tên item.
    - `return`: True nếu item đang bị lỗi, False nếu không.
    - `Example`:
      - checkItemProblem('DaLat_Tanung_GW0',"201X0.1.2")
    '''
    #SCAN ALL HOST
    SORT_PRIO = ["GATEWAY","CONTROLER","SENSOR","TEMP"]
    def sortHost (hostList):
      """Thuật toán:
      - Lấy độ ưu tiên cao nhất trong SORT_PRIO
      - Nhặt hết các host có độ ưu tiên đó ra từ hostList
      - Không quan tâm đến các ký tự số ban đầu trước dấu "_". Sort dựa theo tên các thành phần phía sau.
      - Lặp lại cho các độ ưu tiên còn lại
      - Các host không có độ ưu tiên sẽ được đưa ra sau cùng và sắp xếp theo tên: Không quan tâm đến các ký tự số ban đầu trước dấu "_". Sort dựa theo tên các thành phần phía sau.
      - Gôm các host đã được sắp xếp lại thành 1 list và trả về
      """
      sortedHostList = []
      for prio in SORT_PRIO:
        prioHostList = []
        for host in hostList:
          if prio in host:
            prioHostList.append(host)
        prioHostList.sort(key=lambda x: x.split("_")[1:])
        sortedHostList += prioHostList
      remainHostList = list(set(hostList) - set(sortedHostList))
      remainHostList.sort(key=lambda x: x.split("_")[1:])
      sortedHostList += remainHostList
      return sortedHostList
    
    try:
      #1. GET ALL HOST AND SORT
      allHostQuerry = {
          "method": "host.get",
          "params": {
              "groupids": hostGroupId
          },
          "id": 1
      }
      allHostList = []
      hostIdDict = {} 
      allHostResult = self.zabbix_api.do_request(allHostQuerry["method"], allHostQuerry["params"])["result"]
      for host in allHostResult:
        hostIdDict[host["name"]] = host["hostid"]
      for host in allHostResult:
          allHostList.append(host["name"])
      # print(allHostList)
      sortHostList = sortHost(allHostList)
      # print(sortHostList)
      
      #2. SCAN PROBLEM HOST
      problemHostQuerry = {
          "method": "host.get",
          "params": {
              "groupids": hostGroupId,
              "severities": [2, 5] # 0: not classified; 1: information; 2: warning; 3: average; 4: high; 5: disaster
          },
          "id": 1
      }
      problemHostList = {}
      problemHostResult = self.zabbix_api.do_request(problemHostQuerry["method"], problemHostQuerry["params"])["result"]
      for host in problemHostResult:
          problemHostList[host["name"]] = host
      # print(problemHostList)
      
      #3. RETURN RESULT
      returnList = list()
      for host in sortHostList:
        hostJson = {}
        if host in problemHostList:
          hostJson["name"] = problemHostList[host]["name"]
          hostJson["status"] = "PROBLEM"
          hostJson["problemLink"] = f"http://{zabbixServerIp}/zabbix.php?show=3&show_timeline=1&action=problem.view&groupids%5B%5D={hostGroupId}&hostids%5B%5D={hostIdDict[host]}"
          returnList.append(hostJson)
        else:
          hostJson["name"] = host
          hostJson["status"] = "OK"
          hostJson["problemLink"] = f"http://{zabbixServerIp}/zabbix.php?show=3&show_timeline=1&action=problem.view&groupids%5B%5D={hostGroupId}&hostids%5B%5D={hostIdDict[host]}"
          returnList.append(hostJson)
      return returnList
    except Exception as e:
        logger.error(e)
        return False

################## TESTING #######################
# zabbix_server   = '128.199.153.250'
# zabbix_port     =  10051
# zabbix_user     = 'admin'
# zabbix_password = 'CMEV12345'

# hostGroupName   = "ABC_Customer" 
# hostName        = "DaLat_Tanung_GW0"
# itemName        = "CO2 sensor"
# itemUID         = "201X0.1.2" # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.

# ZABBIX().__init__(zabbix_server, zabbix_port, zabbix_user, zabbix_password)
# ZABBIX().createHostgroup(hostGroupName)
# ZABBIX().createHost(hostGroupName, hostName)
# ZABBIX().createItem(hostName,itemUID,itemName)
# ZABBIX().updateItemValue (hostName, itemUID, 250)



