import time
import paho.mqtt.client as paho
import os
from paho import mqtt

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    # TO-DO: pegar o payload e inserir no banco 
    print(msg.topic + " " + str(msg.qos) + " "+ str(msg.payload))	

client = paho.Client(client_id="servidor")

client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish


host = os.getenv("MQTT_HOST")
client.connect(host)


client.subscribe("pontos/#", qos=1)

# o servidor vai publicar a informacao se o seloneide (sei la como se escreve) pode abrir ou nao
client.publish("pontos/retorno", payload="hot", qos=1)

#client.loop_start()
client.loop_forever()