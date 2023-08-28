import __init
############ IMPORT PARAMETER ############
import sys,os
import re
if os.path.exists("/0_SHARE/myConfiguration.py"): #Mapped from host to container
  MAIN_WORKDIR = sys.path[0]
  os.system("cp /0_SHARE/myConfiguration.py "+MAIN_WORKDIR+"/cloneMyConfig.py")
  os.system("touch "+MAIN_WORKDIR+"/cloneMyConfig.py")
  os.system("touch /0_SHARE/myConfiguration.py")
  from cloneMyConfig import *
else:
  from Application.parameter import *
##########################################
from aiohttp import web
import socketio
# from aiohttp_cors import CorsConfig, ResourceOptions, setup as setup_cors
# from Library.B1_jsonFileControl.jsonFileControl import jsonFileRecord
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt
import threading
import random
import json

class NamespaceConnectionManager:
    def __init__(self):
        self.connections = dict()

    def add_connection(self, sid, namespace):
        self.connections[sid]= namespace

    def remove_connection(self, sid):
        if sid in self.connections:
            del self.connections[sid]

    def get_namespace(self, sid):
        if sid in self.connections:
            return self.connections[sid]
        else:
            return None

# Khởi tạo quản lý kết nối của namespace
connection_manager = NamespaceConnectionManager()


############################################################
# 1. CONNECT TO MQTT BROKER                                #
############################################################
MQTT = mqttClass(MQTT_BROKER_IP, MQTT_PORT, MQTT_CLIENT_SIO_EXCTL_ID, MQTT_USERNAME, MQTT_PASSWORD)
threading.Thread(target=MQTT.listen).start()
##############################################################

############################################################
# 2. CONNECT TO SOCKETIO BROKER                            #
############################################################
sio = socketio.AsyncServer(cors_allowed_origins='*') #Creates a new Async Socket IO Server with cors_allowed_origins='*'
app = web.Application()      #Creates a new Aiohttp Web Application
sio.attach(app)              #Binds our Socket.IO server to our Web App

############################################################
# 3. DEFINE ALL EVENT OF SOCKETIO                          #
############################################################
#Bước 2: Định nghĩa lại các sự kiện của Socket.IO ở đây
##### CONNECT #####
async def __connect(sid,environ,namespace):
    connection_manager.add_connection(sid, namespace)
    print(f'Client connected: {sid}')
    dateTime = datetime.datetime.now().strftime("%H:%M:%S")
    await sio.emit('SERVER_LISTEN',f'[{dateTime}]🚩🚩🚩[{namespace}] Client connected: {sid}',namespace='/SERVER_LISTEN')
    
@sio.event(namespace="/") #Namespace = "/"
async def connect(sid, environ):
    await __connect(sid,environ,namespace='Root')
@sio.event(namespace="/MQTT")
async def connect(sid, environ):
    await __connect(sid,environ,namespace='MQTT')
@sio.event(namespace="/ZABBIX")
async def connect(sid, environ):
    await __connect(sid,environ,namespace='ZABBIX')
@sio.event(namespace="/SERVER_LISTEN")
async def connect(sid, environ):
    await __connect(sid,environ,namespace='SERVER_LISTEN')

##### DISCONNECT #####
@sio.event(namespace="/") #Namespace = "/"
@sio.event(namespace="/MQTT")
@sio.event(namespace="/ZABBIX")
@sio.event(namespace="/SERVER_LISTEN")
async def disconnect(sid):
    namespace = connection_manager.get_namespace(sid)
    if namespace:
        connection_manager.remove_connection(sid)
        print(f'Client connected: {sid}')
        dateTime = datetime.datetime.now().strftime("%H:%M:%S")
        await sio.emit('SERVER_LISTEN',f'[{dateTime}]❌❌❌[{namespace}] Client disconnected: {sid}',namespace='/SERVER_LISTEN')
    else:
        print(f'Client disconnected from unknown namespace: {sid}')

##### RECEIVE MESSAGE #####
import datetime
# Khi nhận được tin nhắn từ client đến trung tâm điều phối tin nhắn: SKRX
async def rootMessageFilter (topic,message,sid,namespace='Root'):
  try:
    message = eval(message) #Num -> string, string same dict -> dict
  except:
    message = str(message) #String -> string
  if type(message) is not dict:
    await sio.emit(topic,message,skip_sid=sid) #Send message to all clients except sender
    dateTime = datetime.datetime.now().strftime("%H:%M:%S")
    await sio.emit('SERVER_LISTEN',f'[{dateTime}]🟢[Root][{topic}] {message}',namespace='/SERVER_LISTEN')
  else:
    if 'method' in message: method = message['method']
    if 'params' in message: params = message['params']
    ######################
    # FILTER MESSAGE     #
    ######################
    # 1. problem.get
    if method == 'problem.get':
      await sio.emit('SOCKET',message,skip_sid=sid,namespace='/ZABBIX') #Send message to all clients except sender
      dateTime = datetime.datetime.now().strftime("%H:%M:%S")
      await sio.emit('SERVER_LISTEN',f'[{dateTime}]🟢[ZABBIX][SOCKET] {message}',namespace='/SERVER_LISTEN')




@sio.event(namespace="/") #Namespace = "/"
async def SOCKET(sid, data:dict):
    #Forward message to SERVER_LISTEN #
    namespace = connection_manager.get_namespace(sid)
    dateTime = datetime.datetime.now().strftime("%H:%M:%S")
    await sio.emit('SERVER_LISTEN',"["+dateTime+"]🔴["+namespace+"][SOCKET] "+str(data),namespace='/SERVER_LISTEN') #Forward message to SERVER_LISTEN
    
    #1.Convert data to JSON
    if type(data) == str:
      jsonData = json.loads(data)
    elif type(data) == dict:
      jsonData = data
    else:
      print("[SOCKET] Received message is not string or dict => Skip message")
      return
    #2.Lan truyền gói tin cho các client khác
    # print(f'[SOCKET] Received message from {sid}: {message}')
    print(f'\n[SOCKET] Received message from {sid}')
    topic   = str(jsonData['topic'])
    message = str(jsonData['message'])
    await rootMessageFilter(topic,message,sid,namespace) #Filter message
    #CHECK LICENSE
    #Compare topic with Regex EXPORT_LICENSE_TO_MQTT_TOPIC_LIST
    for regex in EXPORT_LICENSE_TO_MQTT_TOPIC_LIST:
      if re.search(regex, topic):
        #SEND TO MQTT BROKER
        MQTT.publish(topic=topic, msg=str({"uid": MQTT_CLIENT_SIO_EXCTL_ID,"message":message})) #Send message to MQTT Broker
      
@sio.event(namespace="/MQTT")
@sio.event(namespace="/ZABBIX")
async def SOCKET(sid, data:dict):
    #Forward message to SERVER_LISTEN #
    namespace = connection_manager.get_namespace(sid)
    dateTime = datetime.datetime.now().strftime("%H:%M:%S")
    await sio.emit('SERVER_LISTEN',"["+dateTime+"]🔴["+namespace+"][SOCKET] "+str(data),namespace='/SERVER_LISTEN') #Forward message to SERVER_LISTEN
    
    #1.Convert data to JSON
    if type(data) == str:
      jsonData = json.loads(data)
    elif type(data) == dict:
      jsonData = data
    else:
      print("[SOCKET] Received message is not string or dict => Skip message")
      return
    #2.Lan truyền gói tin cho các client khác
    # print(f'[SOCKET] Received message from {sid}: {message}')
    print(f'\n[SOCKET] Received message from {sid}')
    topic   = str(jsonData['topic'])
    message = str(jsonData['message'])
    await sio.emit(topic,message,skip_sid=sid) #Send message to all clients except sender
          
##################################################################################################
#Bước 3: Cấu hình cho ứng dụng web
async def index(request):
    """Serve the client-side application."""
    with open('/AppDir/Application/WebPage/Web2/testWeb.html') as f:
        return web.Response(text=f.read(), content_type='text/html')
async def socketIoTest(request):
    """Serve the client-side application."""
    with open('/AppDir/Application/WebPage/Web1/socketIoTest.html') as f:
        return web.Response(text=f.read(), content_type='text/html')
# app.router.add_static('/static', 'static')
app.router.add_get('/test', index)
app.router.add_get('/', socketIoTest)


##################################################################################################
### APPLICAITON ROUTER                                                                           #
##################################################################################################
async def SERVER_LISTEN(request):
    with open('/AppDir/Application/WebPage/ServerListen/serverSocketListen.html') as f:
        return web.Response(text=f.read(), content_type='text/html')
app.router.add_get('/listen', SERVER_LISTEN)
##############################
# WEBPAGE: ZABBIX PROBLEM    #
##############################
#COMMON FILES
async def ZBProblem_common_styles(request):
    with open('/AppDir/Application/WebPage/ZBProblem/common/styles.css') as f:
        return web.Response(text=f.read(), content_type='text/css')
app.router.add_get('/ZBProblem/commmon/styles.css', ZBProblem_common_styles)
async def ZBProblem_01C821_script(request):
    with open('/AppDir/Application/WebPage/ZBProblem/common/script.js') as f:
        return web.Response(text=f.read(), content_type='application/javascript')
app.router.add_get('/ZBProblem/commmon/script.js', ZBProblem_01C821_script)

#1. ZBProblem_01C821
async def ZBProblem_01C821(request):
    with open('/AppDir/Application/WebPage/ZBProblem/01C821/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')
app.router.add_get('/ZBProblem_01C821', ZBProblem_01C821)



##################################################################################################
#Check update myConfiguration.py to reboot container
# def checkUpdateMyConfigurationFileToRebootContainer():
#   while True:
#     if os.path.exists("/0_SHARE/myConfiguration.py") and os.path.exists("/AppDir/cloneMyConfig.py"):
#       if os.path.getmtime("/0_SHARE/myConfiguration.py") > os.path.getmtime("/AppDir/cloneMyConfig.py"):
#         print ("myConfiguration.py updated. Rebooting container...")
#         os.system("reboot")
#     time.sleep(5)
# threading.Thread(target=checkUpdateMyConfigurationFileToRebootContainer).start()

if __name__ == '__main__':
    web.run_app(app,port=5000)

    