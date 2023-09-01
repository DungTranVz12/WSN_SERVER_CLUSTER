checkedDate = "2023.08.29"
checkedTime = "23:28:41"

#Input datetime then calculate fromTime and toTime
# fromTime_yyyy_mm_dd_hh_mm = "2023_06_25_00_51"
# toTime_yyyy_mm_dd_hh_mm = "2023_06_25_00_52"
 
import datetime
import time

#Convert date time to epoch
def convertDataTimeToFromToTime(date,time):
  date_time_str = date+" "+time
  date_time_obj = datetime.datetime.strptime(date_time_str, '%Y.%m.%d %H:%M:%S')
  toTime_yyyy_mm_dd_hh_mm = date_time_obj.strftime("%Y_%m_%d_%H_%M")
  #From time = to time - 24h
  fromTime_yyyy_mm_dd_hh_mm = (date_time_obj + datetime.timedelta(hours=-24)).strftime("%Y_%m_%d_%H_%M")
  return fromTime_yyyy_mm_dd_hh_mm,toTime_yyyy_mm_dd_hh_mm

convertDataTimeToFromToTime(checkedDate,checkedTime)