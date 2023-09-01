import __init
# ZABBIX_SERVER   = '157.65.24.169'
# ZABBIX_PORT     = 10051
# ZABBIX_USER     = 'Admin'
# ZABBIX_PASS     = 'zabbix'
# ZABBIX_URL      = 'http://'+ZABBIX_SERVER
from cloneMyConfig import *

import requests.sessions as sessions
import datetime
import base64

def convertDataTimeToFromToTime(date="2023.08.29",time="23:28:41"):
  # checkedDate = "2023.08.29"
  # checkedTime = "23:28:41"
  date_time_str = date+" "+time
  date_time_obj = datetime.datetime.strptime(date_time_str, '%Y.%m.%d %H:%M:%S')
  #Increment 1 seconds to date_time_obj
  date_time_obj = date_time_obj + datetime.timedelta(seconds=1)
  toTime_yyyy_mm_dd_hh_mm_ss = date_time_obj.strftime("%Y_%m_%d_%H_%M_%S")
  #From time = to time - 24h
  fromTime_yyyy_mm_dd_hh_mm_ss = (date_time_obj + datetime.timedelta(hours=-24)).strftime("%Y_%m_%d_%H_%M_%S")
  return fromTime_yyyy_mm_dd_hh_mm_ss,toTime_yyyy_mm_dd_hh_mm_ss

def downloadBase64ZabbixChart(date="2023.08.29",time="23:28:41",itemId="44411"):
    fromTime,toTime = convertDataTimeToFromToTime(date,time)
    fromTimeSplit = fromTime.split("_")
    fromTimeInUrl = fromTimeSplit[0]+"-"+fromTimeSplit[1]+"-"+fromTimeSplit[2]+"%20"+fromTimeSplit[3]+"%3A"+fromTimeSplit[4]+"%3A"+fromTimeSplit[5]
    toTimeSplit = toTime.split("_")
    toTimeInUrl = toTimeSplit[0]+"-"+toTimeSplit[1]+"-"+toTimeSplit[2]+"%20"+toTimeSplit[3]+"%3A"+toTimeSplit[4]+"%3A"+toTimeSplit[5]
    URL_GRAPH = ZABBIX_URL+'/chart.php?from='+fromTimeInUrl+'&to='+toTimeInUrl+'&itemids%5B0%5D='+itemId+'&type=0&profileIdx=web.item.graph.filter&profileIdx2='+itemId+'&width=1082&height=300'
    ULR_LOGIN = ZABBIX_URL+'/index.php?name='+ZABBIX_USER+'&password='+ZABBIX_PASS+'&enter=Sign%20in'
    URL_LINK  = 'http://'+ZABBIX_WEB_OUTSIDE_IP_PORT+'/history.php?action=showgraph&itemids%5B%5D='+itemId+'&from='+fromTimeInUrl+'&to='+toTimeInUrl
    with sessions.Session() as session:
      session.request(method="get", url=ULR_LOGIN)
      response = session.request(method="get", url=URL_GRAPH)
    
    if response.status_code == 200:
      picEncodeBase64 = str(base64.b64encode(response.content),'utf-8')
      return picEncodeBase64,URL_LINK
    else:
      print(f"Failed to download image from {URL_GRAPH}")
      return None,None


# print(downloadBase64ZabbixChart())

