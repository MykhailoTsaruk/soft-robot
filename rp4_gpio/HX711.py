import threading

from RPduino import *

mux = threading.Lock()

class HX711():
    def __init__(self, DOUT: int, SCK: int):
        self.DOUT = DOUT
        self.SCK = SCK
        self.GAIN = 1
        self.OFFSET = 0
        self.RESULT = 0
        self.DESCRIPTION = ''

    def set_RESULT(self, new_RESULT):
        self.RESULT = new_RESULT

    def set_gain(self, new_GAIN):
        self.GAIN = new_GAIN


def is_ready(hx711: HX711) -> bool:
    return digitalRead(hx711.DOUT) == 0

def wait_ready(hx711: HX711, time: int):
    '''
    :param time: time in ms
    :type time: int
    '''
    while(not is_ready(hx711)): delay(time)

def shiftInSlow(dataPin: int, clockPin: int) -> int:

    value = 0

    for i in range(8):
        digitalWrite(clockPin, HIGH)
        delayMicros(1)
        value |= digitalRead(dataPin) << (7 - i)
        digitalWrite(clockPin, LOW)
        delayMicros(1)

    return value

def read(hx711: HX711) -> int:
    wait_ready(hx711, 1)

    value = 0
    data = [0, 0, 0]
    filler = 0x00

    with mux:
        for i in range(3):
            data[2 - i] = shiftInSlow(hx711.DOUT, hx711.SCK)

        for i in range(hx711.GAIN):
            digitalWrite(hx711.SCK, HIGH)
            delayMicros(1)
            digitalWrite(hx711.SCK, LOW)
            delayMicros(1)
    
    filler = 0xFF if data[2] & 0x80 else 0x00

    value = filler  << 8*3  \
          | data[2] << 8*2  \
          | data[1] << 8    \
          | data[0]
    
    return value


            