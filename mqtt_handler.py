import paho.mqtt.client as mqtt
from website import db
from website.models import Dostarczenia, Kurier, Paczka
import time
from threading import Lock
from functools import partial


lock = Lock()


def on_connect(client, userdata, flags, rc):
    client.subscribe("to_central")


class MQTT_handler:
    def __init__(self) -> None:
        self.broker = "192.168.2.10"
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        print("Client_started")

    def start_connection(self):
        self.client.connect_async(self.broker, port=1883, keepalive=60, bind_address="")
        self.client.loop_start()
        # self.client.tls_set("./ca.crt")

    def send(self, topic, message):
        self.client.publish(topic, message, qos=1)

    def add_messege_receive_callback(self, topic_filter, callback):
        self.client.message_callback_add(topic_filter, callback)
        print("Callback added successfully")


def read_dostarczenie_info(client, userdata, message):
    lock.acquire()
    print(message.payload)
    id_kuriera, id_paczki, status = map(int, message.payload.decode("utf-8") .split(","))
    kurier = Kurier.query.filter_by(id=id_kuriera).first()
    paczka = Paczka.query.filter_by(id=id_paczki).first()

    if not paczka:
        paczka = Paczka(id=id_paczki, nazwa=f"Paczka: {id_paczki}")
        db.session.add(paczka)
        db.session.commit()

        if status == 1:
            dostarczenie = Dostarczenia(
                kurier_id=kurier.id, paczka_id=paczka.id, status="nadana"
            )
            db.session.add(dostarczenie)
            db.session.commit()
            client.publish(
                "to_terminal", f"{id_kuriera},ok,package sent successfully"
            )
        else:
            client.publish(
                "to_terminal", f"{id_kuriera},error,package has to be sent first"
            )
    else:
        dostarczenie = Dostarczenia.query.filter_by(kurier_id=kurier.id, paczka_id=paczka.id).first()
        if not dostarczenie:
            if status == 1:
                dostarczenie = Dostarczenia(
                    kurier_id=kurier.id, paczka_id=paczka.id, status="nadana"
                )
                db.session.add(dostarczenie)
                db.session.commit()
                client.publish(
                    "to_terminal", f"{id_kuriera},ok,package sent successfully"
                )
            else:
                client.publish(
                    "to_terminal", f"{id_kuriera},error,package has to be sent first"
                )
        else:
            if status == 2:
                dostarczenie.status = "dostarczona"
                db.session.commit()
                client.publish(
                    "to_terminal", f"{id_kuriera},ok,package received successfully"
                )
            else:
                client.publish(
                    "to_terminal", f"{id_kuriera},error,package cannot be sent twice"
                )

    lock.release()


def add_mqtt_client():
    lock = Lock()
    mqtt_handler = MQTT_handler()
    time.sleep(2)
    mqtt_handler.start_connection()
    time.sleep(2)
    mqtt_handler.add_messege_receive_callback(
        "to_central", read_dostarczenie_info,
    )
    return mqtt_handler
