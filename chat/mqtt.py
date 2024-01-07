import time

import paho.mqtt.client as mqtt
from django.conf import settings


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('bpp-1')
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    
def on_disconnect(client, userdata, rc):
    print.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, settings.MQTT_FIRST_RECONNECT_DELAY
    while reconnect_count < settings.MQTT_MAX_RECONNECT_COUNT:
        print.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            print.info("Reconnected successfully!")
            return
        except Exception as err:
            print.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= settings.MQTT_RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, settings.MQTT_MAX_RECONNECT_DELAY)
        reconnect_count += 1
    print.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)    

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)