#################################################
#  HP1 PC                                       #
#################################################
ZABBIX_WEB_OUTSIDE_IP_PORT = "lotus1104.synology.me:10002" #HP1

################### MySQL DEFINE ########################
MYSQL_HOST     = "wsnCluster_zabbix-mysql-server"
MYSQL_DATABASE = "zabbix"
MYSQL_USER     = "root"
MYSQL_PASS     =  "root_pwd"
################### ZABBIX DEFINE #######################
ZABBIX_SERVER       = 'wsnCluster_zabbix-server-agent'
ZABBIX_WEB_IP       = 'wsnCluster_zabbix-web-nginx-mysql'
ZABBIX_WEB_PORT     = '8080'
ZABBIX_PORT         = 10051
ZABBIX_USER         = 'Admin'
ZABBIX_PASS         = 'zabbix'
ZABBIX_URL          = 'http://'+ZABBIX_WEB_IP+':'+ZABBIX_WEB_PORT
ZABBIX_MYSQL_UPLOAD = True #Upload data to MySQL directly. Not user Zabbix Sender Library.
################### MQTT DEFINE #######################
import random
MQTT_BROKER_IP  = "wsnCluster_mqtt"
MQTT_PORT       = 1885
MQTT_USERNAME   = "mqtt_broker"
MQTT_PASSWORD   = "!Da#ImU%VuF3V"
MQTT_CLIENT_ID  = f'MQTT_CLENT_JP_'+str(random.randint(0, 10000))
MQTT_TOPIC      = "WSN_SVR_JP_REQ" 

################### SOCKETIO #######################
# LICENSE TO EXPORT TO MQTT NETWORK
MQTT_CLIENT_SIO_EXCTL_ID       = f'SIO_EXCTL_'+str(random.randint(0, 10000)) #NOTE: DO NOT CHANGE THIS ID
EXPORT_LICENSE_TO_MQTT_TOPIC_LIST = list()  #List of TOPICs licensed to publish to the MQTT network.
EXPORT_LICENSE_TO_MQTT_TOPIC_LIST.append(".*WEB.*")  #Regex pattern. Allowing all topic include WEB in the topic name.


# LICENSE TO EXPORT TO SOCKETIO NETWORK
MQTT_CLIENT_MQTT_EXCTL_ID          = f'MQTT_EXCTL_'+str(random.randint(0, 10000)) #NOTE: DO NOT CHANGE THIS ID
EXPORT_LICENSE_TO_SOCKETIO_TOPIC_LIST = list()  #List of TOPICs licensed to publish to the SOCKETIO network.
EXPORT_LICENSE_TO_SOCKETIO_TOPIC_LIST.append(".*WEB.*")  #Regex pattern. Allowing all topic include WEB in the topic name.
EXPORT_LICENSE_TO_SOCKETIO_TOPIC_LIST.append(".*GATEWAY\.CONTROL.*")  #Regex pattern. Allowing all topic include GATEWAY.CONTROL in the topic name.


SOCKETIO_URL = f'http://wsnCluster_socketio:5000' # EX: "http://lotus1104.synology.me:83"

################## ACCEPT LIST OF GATEWAY & TOPIC #######################
# PURPOSE: Create a list of Gateways and Topics that the MQTT Client can subscribe to
# NOTE: MQTT TOPIC FORMAT: <GATEWAY_ID>.<TOPIC>
# EX: WSN_GW_01C823.WEB.SCAN_PROBLEM
# EX: WSN_GW_01C823.WEB.SCAN_REDTIDE
ACCEPT_LIST_OF_TOPIC = list()
#===============================================================================
# 1. ACCEPT LIST OF GATEWAY    #<------ ADD THE NEW GATEWAY HERE
#===============================================================================
ACCEPT_LIST_OF_GATEWAY = list()
ACCEPT_LIST_OF_GATEWAY.append("WSN_GW_01C823")
ACCEPT_LIST_OF_GATEWAY.append("WSN_GW_01C821") #Seaside Consulting customer
ACCEPT_LIST_OF_GATEWAY.append("WSN_GW_018F1A") #Sugaya customer
ACCEPT_LIST_OF_GATEWAY.append("WSN_GW_320DED") #CMEV office test

#===============================================================================
# 2. ACCEPT LIST OF TOPIC    #<------ DEVELOPER ADD THE NEW TOPIC HERE
#===============================================================================
# 2.1 WEB.xxx topic: the request issued from the web
ACCEPT_LIST_OF_TOPIC.append("WEB.SCAN_PROBLEM")  #Topic use for scan problem
ACCEPT_LIST_OF_TOPIC.append("WEB.SCAN_REDTIDE")  #Topic use for scan redtide
ACCEPT_LIST_OF_TOPIC.append("WEB.CONTROL")       #Topic use for control controller node (issue from web)
ACCEPT_LIST_OF_TOPIC.append("WEB.TEST")          #Topic use for testing

# 2.2 GATEWAY.xxx topic: the request issued from the gateway
ACCEPT_LIST_OF_TOPIC.append("GATEWAY.CONTROL")   #Topic use for update control status to web (issue from gateway)




