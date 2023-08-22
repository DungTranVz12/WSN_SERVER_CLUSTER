########## 1. MQTT Server ##########
# ################## ZABBIX DEFINE #######################
ZABBIX_SERVER   = '157.65.24.169'
ZABBIX_PORT     = 10051
ZABBIX_USER     = 'Admin'
ZABBIX_PASS     = 'zabbix'
ZABBIX_URL      = 'http://'+ZABBIX_SERVER
# ################## ZABBIX DEFINE #######################
import random
MQTT_BROKER_IP                 = "lotus1104.synology.me"
MQTT_PORT                      = 1885
MQTT_USERNAME                  = "mqtt_broker"
MQTT_PASSWORD                  = "!Da#ImU%VuF3V"
MQTT_CLIENT_ID                 = f'MQTT_CLENT_JP_'+str(random.randint(0, 10000))
MQTT_TOPIC                     = "WSN_SVR_JP_REQ"

################### SOCKETIO #######################
MQTT_EXPORT_LICENSE_TOPIC_LIST = list()  #Danh sách các TOPIC có giấy phép để publish đến mạng MQTT.
MQTT_EXPORT_LICENSE_TOPIC_LIST.append("WSN_GW_01C823")  
MQTT_CLIENT_SIO_EXCTL_ID       = f'SIO_EXCTL_'+str(random.randint(0, 10000))
SOCKETIO_EXPORT_LICENSE_TOPIC_LIST = list()  #Danh sách các TOPIC có giấy phép để publish đến mạng MQTT.
SOCKETIO_EXPORT_LICENSE_TOPIC_LIST.append("WSN_GW_01C823")  
MQTT_CLIENT_MQTT_EXCTL_ID          = f'MQTT_EXCTL_'+str(random.randint(0, 10000))
SOCKETIO_URL = "http://100.100.100.4:5000" # EX: "http://lotus1104.synology.me:83"