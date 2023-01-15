import paho.mqtt.client as mqtt

class MQTT_handler:
    def __init__(self) -> None:
        self.broker = "localhost"
        self.client = mqtt.Client()

    def start_connection(self):
        self.client.connect_async(self.broker, port=1883, keepalive=60, bind_address="")
        self.client.loop_start()
        
    def send(self, topic, message):
        self.publish(topic, message, qos=1)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def add_messege_receive_callback(self, topic_filter, callback):
        self.client.message_callback_add(topic_filter, callback)