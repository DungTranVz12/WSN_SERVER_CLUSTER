############################################################
# USER CONFIGURATION                                       #
############################################################
import random
MQTT_EXPORT_LICENSE_TOPIC_LIST = list()  #Danh sách các TOPIC có giấy phép để publish đến mạng MQTT.
MQTT_EXPORT_LICENSE_TOPIC_LIST.append("WSN_GW_01C823")  
MQTT_BROKER_IP = "lotus1104.synology.me"
MQTT_PORT = 1885
MQTT_USERNAME = "mqtt_broker"
MQTT_PASSWORD = "!Da#ImU%VuF3V"
MQTT_CLIENT_SIO_ID = f'SIO_EXCTL_'+str(random.randint(0, 10000))