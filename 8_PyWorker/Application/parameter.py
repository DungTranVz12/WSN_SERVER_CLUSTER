# ################## ZABBIX DEFINE #######################
ZABBIX_SERVER   = '157.65.24.169'
ZABBIX_PORT     = 10051
ZABBIX_USER     = 'Admin'
ZABBIX_PASS     = 'zabbix'
ZABBIX_URL      = 'http://'+ZABBIX_SERVER
# ################## ZABBIX DEFINE #######################
import random
MQTT_BROKER_IP = "lotus1104.synology.me"
MQTT_PORT      = 1885
MQTT_USERNAME  = "mqtt_broker"
MQTT_PASSWORD  = "!Da#ImU%VuF3V"
MQTT_CLIENT_ID = f'MQTT_SOCKET_CLIENT_JP_'+str(random.randint(0, 10000))
MQTT_TOPIC     = "WSN_SVR_JP_REQ"


PROFILE_MANAGER = "/myConfig" #Ignore this. This is for the profile manager
TRANS_DATA_DIR = "/myConfig" #Ignore this. This is for the profile manager