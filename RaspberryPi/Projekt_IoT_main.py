
from enum import Enum
from time import sleep
from mqtt_handler import MQTT_handler
from config import *
import RPi.GPIO as GPIO
from rpi_functions import *

class Terminal_state(Enum):
    GETTING_PACKAGE = 1
    GIVING_PACKAGE = 2
    IDLE = 3
    WAITING = 4

class Red_button_callback:
    def __init__(self, terminal):
        self.terminal = terminal

    def __call__(self, channel):
        self.terminal.current_menu_option = (self.terminal.current_menu_option + 1) % len(self.terminal.menu_options)
        self.terminal.draw_menu()

class Green_button_callback:
    def __init__(self, terminal):
        self.terminal = terminal

    def __call__(self, channel):
        if self.terminal.state != Terminal_state.IDLE:
            return

        if self.terminal.current_menu_option == 0:
            self.terminal.state = Terminal_state.GETTING_PACKAGE
            #wyswietl wiadomosc na ekranie aby przylozyc karte
        elif self.terminal.current_menu_option == 1:
            self.terminal.state = Terminal_state.GIVING_PACKAGE
            #wysiwetl wiadomosc na ekranie aby przylozyc karte

class Message_package_callback:
    def __init__(self, terminal):
        self.terminal = terminal

    def __call__(self, client, userdata, message):
        #if courier_id != self.terminal.courier_id
        #    return

        #if message_ok:
        #   wyswietl ok
        #   rpi_functions.short_buzz()
        #   rpi_functions.flash_led_stripe((0, 255, 0), 0.3)
        #elif message_not_ok:
        #   wyswietl nie ok
        #   rpi_functions.short_buzz()
        #   rpi_functions.flash_led_stripe((255, 0, 0) 0.3)
        sleep(2)
        self.terminal.state = Terminal_state.IDLE
        #redraw menu
        pass

#mozna zignorowac
class Message_courier_callback:
    def __init__(self, terminal):
        self.terminal = terminal

    def __call__(self, client, userdata, message):
        #sprawdz czy to message do mnie na podstawie maca
        #wyswietl komunikat o zmianie id kuriera
        self.terminal.mqtt_handler.send(#topic, #wiadomosc_zwrotna)
        sleep(1)
        #redraw menu
        pass

class Terminal:
    def __init__(self):
        #ze statem będzie prawdopodobnie data race
        self.state = Terminal_state.IDLE
        #z courier_id pewnie też data race albo nie jesli nie bedzie zmieniany
        self.courier_id = 1
        self.current_menu_option = 0
        self.menu_options = [ "Odbierz paczkę", "Wydaj paczkę" ]
        self.mqtt_handler = MQTT_handler()
        GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=Red_button_callback(self), bouncetime=200) 
        GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=Green_button_callback(self), bouncetime=200) 
        self.mqtt_handler.add_messege_receive_callback("terminal/operation/#", Message_package_callback(self))
        self.mqtt_handler.add_messege_receive_callback("terminal/courier/change", Message_courier_callback(self))


    def draw_menu(self):
        menu(self.current_menu_option)


    def rfid_callback(id):
        payload = f"{self.courier_id};{id}"
        if self.state == Terminal_state.GIVING_PACKAGE:
            self.mqtt_handler.send("give", payload)
        elif self.state == Terminal_state.GETTING_PACKAGE:
            self.mqtt_handler.send("get", payload)
        self.state = Terminal_state.WAITING
    

    def main_loop(self):
        read_rfid_loop(rfid_callback)


def main():
    terminal = Terminal()
    terminal.mqtt_handler.start_connection()
    oled_welcome()
    time.sleep(2)
    terminal.draw_menu()
    terminal.main_loop()
        

if __name__ == "__main__":
    main()