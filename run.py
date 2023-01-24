from website import app
from mqtt_handler import add_mqtt_client
import time


if __name__ == '__main__':
    mqtt_handler = add_mqtt_client()
    app.run(debug=True)
    while True:
        time.sleep(0.1)
