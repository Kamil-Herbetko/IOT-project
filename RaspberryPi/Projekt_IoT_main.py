from enum import Enum
from time import sleep
from mqtt_handler import MQTT_handler
from config import *
import RPi.GPIO as GPIO
from rpi_functions import *

COURIER_ID = 1


class Terminal_state(Enum):
    GETTING_PACKAGE = 1
    GIVING_PACKAGE = 2
    IDLE = 3
    WAITING = 4

class Red_button_callback:
    def __init__(self, terminal):
        self.terminal = terminal

    def __call__(self, channel):
        if self.terminal.state != Terminal_state.IDLE:
            return 

        self.terminal.current_menu_option = (self.terminal.current_menu_option + 1) % 2
        self.terminal.draw_menu()

class Green_button_callback:
    def __init__(self, terminal):
        self.terminal = terminal

    def __call__(self, channel):
        if self.terminal.state in [Terminal_state.GETTING_PACKAGE, Terminal_state.GIVING_PACKAGE]:
            self.terminal.state = Terminal_state.IDLE
            menu(self.terminal.current_menu_option)

        if self.terminal.state != Terminal_state.IDLE:
            return

        if self.terminal.current_menu_option == 0:
            self.terminal.state = Terminal_state.GETTING_PACKAGE
            oled_take_package_screen()
        elif self.terminal.current_menu_option == 1:
            self.terminal.state = Terminal_state.GIVING_PACKAGE
            oled_delivery_package_screen()

class Message_package_callback:
    OK_SIGNAL = 0
    NOOK_SIGNAL = 1
    
    def __init__(self, terminal):
        self.terminal = terminal

    def __call__(self, client, userdata, message):
        package_info = message.payload.split(",")

        if int(package_info[0]) != self.terminal.courier_id:
            return

        if int(package_info[2]) == self.OK_SIGNAL:
            oled_accept_package()
            short_buzz()
            flash_led_stripe((0, 255, 0), 0.3)
        elif int(package_info[2]) == self.NOOK_SIGNAL:
            oled_decline_package()
            long_buzz()
            flash_led_stripe((255, 0, 0), 0.3)
        
        sleep(2)
        self.terminal.state = Terminal_state.IDLE
        self.terminal.draw_menu()


""" class Message_courier_callback:
    def __init__(self, terminal):
        self.terminal = terminal

    def __call__(self, client, userdata, message):
        #sprawdz czy to message do mnie na podstawie maca
        #wyswietl komunikat o zmianie id kuriera
        #self.terminal.mqtt_handler.send(#topic, #wiadomosc_zwrotna)
        sleep(1)
        #redraw menu
        pass
 """
class Terminal:
    def __init__(self):
        #ze statem będzie prawdopodobnie data race
        self.state = Terminal_state.IDLE
        #z courier_id pewnie też data race albo nie jesli nie bedzie zmieniany
        self.courier_id = COURIER_ID
        self.current_menu_option = 0
        #self.menu_options = [ "Odbierz paczkę", "Wydaj paczkę" ]
        self.mqtt_handler = MQTT_handler()
        GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=Red_button_callback(self), bouncetime=200) 
        GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=Green_button_callback(self), bouncetime=200) 
        self.mqtt_handler.add_messege_receive_callback("to_terminal", Message_package_callback(self))
        #self.mqtt_handler.add_messege_receive_callback("terminal/courier/change", Message_courier_callback(self))

    def draw_menu(self):
        menu(self.current_menu_option)

    def rfid_callback(self, id):
        if self.state in [Terminal_state.GETTING_PACKAGE, Terminal_state.GIVING_PACKAGE]:
            payload = f"{self.courier_id},{id},{self.state}"
            self.mqtt_handler.send("to_central", payload)
            self.state = Terminal_state.WAITING
    
    def main_loop(self):
        read_rfid_loop(self.rfid_callback)


def main():
    terminal = Terminal()
    terminal.mqtt_handler.start_connection()
    oled_welcome()
    time.sleep(2)
    terminal.draw_menu()
    terminal.main_loop()

if __name__ == "__main__":
    main()