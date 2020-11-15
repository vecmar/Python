from microbit import *

uart.init(baudrate=115200, tx=None, rx=None)

while True:
    if button_a.is_pressed():
        print("9999")
    if button_b.is_pressed():
        print("8888")
    x = accelerometer.get_x()
    print(x)
    sleep(20)