import time
from config import *
from mfrc522 import MFRC522
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
import board
import neopixel

def id(uid: list[int]):
    id = 0
    for i in range(0, len(uid)):
        id += uid[i] << (i*8)
    return id

def read_rfid():
    last_id = None
    while True:
        MIFAREReader = MFRC522()
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK and last_id != id(uid):
                last_id = id(uid)
                return id(uid)
        else:
            last_id = None

def buzzer(state):
    GPIO.output(buzzerPin, not state)

def buzzer_beep(beep_period: float):
    buzzer(True)
    time.sleep(beep_period)
    buzzer(False)

def short_buzz():
    buzzer_beep(0.3)

def long_buzz():
    buzzer_beep(0.7)

def led_setup():
    pixels = neopixel.NeoPixel(
        board.D18, 8, brightness=1.0/32, auto_write=False)
    pixels.fill((255, 0, 0))
    pixels.show()

def flash_led_stripe(color: tuple[int, int, int], flash_period: float):
    pixels = neopixel.NeoPixel(
        board.D18, 8, brightness=1.0/32, auto_write=False)
    pixels.fill(color)
    pixels.show()
    time.sleep(flash_period)
    pixels.fill((0, 0, 0))
    pixels.show()

def buttons_setup():
    GPIO.add_event_detect(buttonGreen, GPIO.RISING, callback=handle_buttons, bouncetime=200)

def handle_buttons():
    if GPIO.input(buttonRed) == 1:
        handle_red_button()
    if GPIO.input(buttonGreen) == 1:
        handle_green_button()

def handle_green_button(onPress):
    onPress()

def handle_red_button(onPress):
    onPress()

def oled_setup():
    disp = SSD1331.SSD1331()
    disp.Init()
    disp.clear()
    return disp

def init_oled_canvas():
    disp = oled_setup()    
    canvas = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(canvas)
    fontLarge = ImageFont.truetype('./lib/oled/Font.ttf', 30)
    fontSmall = ImageFont.truetype('./lib/oled/Font.ttf', 12)
    return disp, canvas, draw, fontLarge, fontSmall

def oled_welcome():
    disp, canvas, draw, fontLarge, fontSmall = oled_setup()
    draw.rectangle([(0, 0), (96, 64)], fill="YELLOW")
    draw.text((8, 0), u'Witaj', font=fontLarge, fill="WHITE")
    draw.text((12, 40), 'w systemie obsługi kurierskiej', font=fontSmall, fill="WHITe")
    disp.ShowImage(canvas, 0, 0)

def oled_take_package_screen():
    disp, canvas, draw, fontLarge, fontSmall = oled_setup()
    draw.rectangle([(0, 0), (96, 64)], fill="NAVY")
    draw.text((8, 0), u'Pobieranie paczek', font=fontLarge, fill="WHITE")
    disp.ShowImage(canvas, 0, 0)

def oled_delivery_package_screen():
    disp, canvas, draw, fontLarge, fontSmall = oled_setup()
    draw.rectangle([(0, 0), (96, 64)], fill="NAVY")
    draw.text((8, 0), u'Wydawanie paczek', font=fontLarge, fill="WHITE")
    disp.ShowImage(canvas, 0, 0)

def oled_accept_package(info: str):
    disp, canvas, draw, fontLarge, fontSmall = oled_setup()
    draw.rectangle([(0, 0), (96, 64)], fill="LIME")
    draw.text((0, 0), u'Paczka zaakceptowana', font=fontLarge, fill="WHITE")
    draw.text((30, 0), f'{info}', font=fontSmall, fill="WHITE")
    draw.text((45, 0), u'✔️', font=fontLarge, fill="GREEN")
    disp.ShowImage(canvas, 0, 0)

def oled_decline_package(info: str):
    disp, canvas, draw, fontLarge, fontSmall = oled_setup()
    draw.rectangle([(0, 0), (96, 64)], fill="MAROON")
    draw.text((0, 0), u'Paczka odrzucona', font=fontLarge, fill="WHITE")
    draw.text((30, 0), f'{info}', font=fontSmall, fill="WHITE")
    draw.text((45, 0), u'❌', font=fontLarge, fill="RED")
    disp.ShowImage(canvas, 0, 0)

if __name__ == "__main__":
    flash_led_stripe((255, 0, 255), 1)
    pass