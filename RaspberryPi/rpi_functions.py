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
    return str(id)

def read_rfid_loop(func):
    last_id = None
    while True:
        MIFAREReader = MFRC522()
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK and last_id != id(uid):
                last_id = id(uid)
                func(id(uid))
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

def handle_green_button(handle_button):
    GPIO.add_event_detect(buttonGreen, GPIO.RISING, callback=handle_button, bouncetime=200)

def handle_red_button(handle_button):
    GPIO.add_event_detect(buttonGreen, GPIO.RISING, callback=handle_button, bouncetime=200)

def oled_setup():
    disp = SSD1331.SSD1331()
    disp.Init()
    disp.clear()
    return disp

def init_oled_canvas():
    disp = oled_setup()
    canvas = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(canvas)
    fontLarge = ImageFont.truetype('./lib/oled/Font.ttf', 16)
    fontSmall = ImageFont.truetype('./lib/oled/Font.ttf', 12)
    return disp, canvas, draw, fontLarge, fontSmall

def oled_welcome():
    disp, canvas, draw, fontLarge, fontSmall = init_oled_canvas()
    draw.rectangle([(1, 1), (94, 62)], fill="YELLOW")
    draw.text((4, 0), u'Witaj', font=fontLarge, fill="WHITE")
    draw.text((6, 26), 'w systemie \nkurierskim', font=fontSmall, fill="WHITe")
    disp.ShowImage(canvas, 0, 0)

def oled_take_package_screen():
    disp, canvas, draw, fontLarge, fontSmall = init_oled_canvas()
    draw.rectangle([(1, 1), (94, 62)], fill="NAVY")
    draw.text((2, 0), u'Pobieranie\npaczek', font=fontLarge, fill="WHITE")
    disp.ShowImage(canvas, 0, 0)

def oled_delivery_package_screen():
    disp, canvas, draw, fontLarge, fontSmall = init_oled_canvas()
    draw.rectangle([(1, 1), (94, 62)], fill="NAVY")
    draw.text((2, 0), u'Wydawanie\npaczek', font=fontLarge, fill="WHITE")
    disp.ShowImage(canvas, 0, 0)

def oled_accept_package(info: str):
    disp, canvas, draw, fontLarge, fontSmall = init_oled_canvas()
    draw.rectangle([(1, 1), (94, 62)], fill="LIME")
    draw.text((4, 0), u'Paczka\nokej', font=fontLarge, fill="WHITE")
    draw.text((4, 42), f'{info}', font=fontSmall, fill="GREEN")
    disp.ShowImage(canvas, 0, 0)

def oled_decline_package(info: str):
    disp, canvas, draw, fontLarge, fontSmall = init_oled_canvas()
    draw.rectangle([(1, 1), (94, 62)], fill="MAROON")
    draw.text((4, 0), u'Paczka\nodrzucona', font=fontLarge, fill="WHITE")
    draw.text((4, 42), f'{info}', font=fontSmall, fill="RED")
    disp.ShowImage(canvas, 0, 0)

def menu(opt: int):
    disp, canvas, draw, fontLarge, fontSmall = init_oled_canvas()
    draw.rectangle([(0, 0), (95, 64)], fill="gray")
    if opt == 1:
        draw.rectangle([(0, 0), (48, 64)], fill="seagreen")
    if opt == 2:
        draw.rectangle([(48, 0), (96, 64)], fill="orangered")
    
    draw.rectangle([(4, 4), (42, 60)], fill="palegreen")
    draw.rectangle([(52, 4), (92, 60)], fill="tomato")
    
    take_img = Image.open('./take.png').resize((40, 40)).convert("RGBA")
    delivery_img = Image.open('./delivery.png').resize((40, 40)).convert("RGBA")
    canvas.paste(take_img, (4, 10))
    canvas.paste(delivery_img, (52, 10))
    
    disp.ShowImage(canvas, 0, 0)

if __name__ == "__main__":
    menu(1)
    time.sleep(2)
    menu(2)