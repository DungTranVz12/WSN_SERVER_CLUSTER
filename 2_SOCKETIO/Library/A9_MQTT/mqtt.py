import __init
from paho.mqtt import client as mqtt_client #pip install paho-mqtt
import random

class mqttClass ():
    def __init__(self, broker="", port=1883, client_id=f"ClientId_{random.randint(0, 1000)}", username="not_required", password="not_required"):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = mqtt_client.Client(client_id)
        self.client.username_pw_set(username, password)
        self.client.connect(broker, port)

    def msgRcvFilter(self,msg):
        pass

    def on_message(self, client, userdata, msg):
        print(f"MQTT received `{msg.payload.decode()}` from `{msg.topic}` topic.")
        self.msgRcvFilter(msg)

    def publish(self, topic, msg):
        self.client.publish(topic, msg)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
    
    def listen(self):
        self.client.on_message = self.on_message
        self.client.loop_forever()