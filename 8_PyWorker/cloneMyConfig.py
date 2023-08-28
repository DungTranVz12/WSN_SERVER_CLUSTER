#################################################
#  MAC PC                                       #
#################################################
ZABBIX_WEB_OUTSIDE_IP_PORT = "lotus1104.synology.me:10002" #MAC PC

########## 1. MQTT Server ##########
# ################## ZABBIX DEFINE #######################
ZABBIX_SERVER   = 'wsnCluster_zabbix-server-agent'
ZABBIX_WEB_IP   = 'wsnCluster_zabbix-web-nginx-mysql'
ZABBIX_WEB_PORT = '8080'
ZABBIX_PORT     = 10051
ZABBIX_USER     = 'Admin'
ZABBIX_PASS     = 'zabbix'
ZABBIX_URL      = 'http://'+ZABBIX_WEB_IP+':'+ZABBIX_WEB_PORT
# ################## ZABBIX DEFINE #######################
import random
MQTT_BROKER_IP  = "wsnCluster_mqtt"
MQTT_PORT       = 1885
MQTT_USERNAME   = "mqtt_broker"
MQTT_PASSWORD   = "!Da#ImU%VuF3V"
MQTT_CLIENT_ID  = f'MQTT_CLENT_JP_'+str(random.randint(0, 10000))
MQTT_TOPIC      = "WSN_SVR_JP_REQ"

################### SOCKETIO #######################
EXPORT_LICENSE_TO_MQTT_TOPIC_LIST = list()  #Danh sách các TOPIC có giấy phép để publish đến mạng MQTT.
EXPORT_LICENSE_TO_MQTT_TOPIC_LIST.append("WSN_GW_01C823")  
MQTT_CLIENT_SIO_EXCTL_ID       = f'SIO_EXCTL_'+str(random.randint(0, 10000))

EXPORT_LICENSE_TO_SOCKETIO_TOPIC_LIST = list()  #Danh sách các TOPIC có giấy phép để publish đến mạng MQTT.
EXPORT_LICENSE_TO_SOCKETIO_TOPIC_LIST.append("WSN_GW_01C823")  
MQTT_CLIENT_MQTT_EXCTL_ID          = f'MQTT_EXCTL_'+str(random.randint(0, 10000))

SOCKETIO_URL = f'http://200.200.200.7:5000' # EX: "http://lotus1104.synology.me:83"