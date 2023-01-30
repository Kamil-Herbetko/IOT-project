import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe("to_terminal")

class MQTT_handler:
    def __init__(self) -> None:
        self.broker = "Kamil_Mobile.local"
        self.client = mqtt.Client()
        self.client.on_connect = on_connect

    def start_connection(self):
        self.client.connect_async(self.broker, port=1883, keepalive=60, bind_address="")
        #self.client.tls_set("./ca.crt")
        self.client.loop_start()
        
    def send(self, topic, message):
        self.client.publish(topic, message, qos=1)

    def add_messege_receive_callback(self, topic_filter, callback):
        self.client.message_callback_add(topic_filter, callback)