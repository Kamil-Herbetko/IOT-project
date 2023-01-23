import paho.mqtt.client as mqtt
from website import db 
from website.models import Dostarczenia, Kurier, Paczka


class MQTT_handler:
    def __init__(self) -> None:
        self.broker = "Kamil_Mobile.local"
        self.client = mqtt.Client()

    def start_connection(self):
        self.client.connect_async(self.broker, port=1883, keepalive=60, bind_address="")
        self.client.loop_start()
        self.client.tls_set("./ca.crt")

    def send(self, topic, message):
        self.client.publish(topic, message, qos=1)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def add_messege_receive_callback(self, topic_filter, callback):
        self.client.message_callback_add(topic_filter, callback)


def read_dostarczenie_info(client, userdata, message):
    id_kuriera, id_paczki, status = map(int, message.payload.split(","))
    kurier = Kurier.query.filter_by(id=id_kuriera).first()
    paczka = Paczka.query.filter_by(id=id_paczki).first()

    if not paczka:
        paczka = Paczka(id=id_paczki, nazwa=f'Paczka: {id_paczki}')
        db.session.add(paczka)
        db.session.commit()

        if message == 1:
            dostarczenie = Dostarczenia(kurier_id=kurier.id, paczka_id=paczka.id, status="Nadana")
            
        else:
            client.publish()


def add_mqtt_client():
    mqtt_handler = MQTT_handler()
    mqtt_handler.add_messege_receive_callback("paczka/status/change", read_dostarczenie_info)
    
