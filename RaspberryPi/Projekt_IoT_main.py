
from enum import Enum
from time import sleep
from mqtt_handler import MQTT_handler
from config import *
import RPi.GPIO as GPIO
import rpi_functions

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
            rpi_functions.oled_take_package_screen()
        elif self.terminal.current_menu_option == 1:
            self.terminal.state = Terminal_state.GIVING_PACKAGE
            rpi_functions.oled_delivery_package_screen()

class Message_package_callback:
    def __init__(self, terminal):
        self.terminal = terminal

    def __call__(self, client, userdata, message):
        package_info = message.payload.split(",")

        if int(package_info[0]) != self.terminal.courier_id:
            return

        if package_info[2] == 0:#message_ok
            rpi_functions.oled_accept_package("")
            rpi_functions.short_buzz()
            rpi_functions.flash_led_stripe((0, 255, 0), 0.3)
        elif package_info[2] == 1:#message_not_ok
            rpi_functions.oled_decline_package("")
            rpi_functions.short_buzz()
            rpi_functions.flash_led_stripe((255, 0, 0), 0.3)
        sleep(2)
        self.terminal.state = Terminal_state.IDLE
        self.terminal.draw_menu()

#mozna zignorowac
class Message_courier_callback:
    def __init__(self, terminal):
        self.terminal = terminal

    def __call__(self, client, userdata, message):
        #sprawdz czy to message do mnie na podstawie maca
        #wyswietl komunikat o zmianie id kuriera
        #self.terminal.mqtt_handler.send(#topic, #wiadomosc_zwrotna)
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
        #self.menu_options = [ "Odbierz paczkę", "Wydaj paczkę" ]
        self.mqtt_handler = MQTT_handler()
        GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=Red_button_callback(self), bouncetime=200) 
        GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=Green_button_callback(self), bouncetime=200) 
        self.mqtt_handler.add_messege_receive_callback("to_terminal", Message_package_callback(self))
        #self.mqtt_handler.add_messege_receive_callback("terminal/courier/change", Message_courier_callback(self))


    def draw_menu(self):
        rpi_functions.menu(self.current_menu_option)

    def read_rfid(self):
        id = rpi_functions.read_rfid()
        #dodac jakis timeout do rfida
        topic = "to_central"
        
        self.mqtt_handler.send(topic, str(self.courier_id) + ";" + str(id))
        self.state = Terminal_state.WAITING

    def main_loop(self):
        while True:
            if self.state == Terminal_state.GIVING_PACKAGE or self.state == Terminal_state.GETTING_PACKAGE:
                self.read_rfid()
                #jesli zbyt dlugo nie ma przylozonej karty to wroc do idle state
            else:
                sleep(0.1)


def main():
    terminal = Terminal()
    terminal.mqtt_handler.start_connection()
    terminal.draw_menu()
    terminal.main_loop()
        

if __name__ == "__main__":
    main()