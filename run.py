from website import app
from mqtt_handler import add_mqtt_client


if __name__ == '__main__':
    add_mqtt_client()
    app.run(debug=True)
