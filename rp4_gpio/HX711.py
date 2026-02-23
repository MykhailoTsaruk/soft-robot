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

        pinMode(self.DOUT, INPUT)
        pinMode(self.SCK, OUTPUT)

    def get_result(self) -> int:
        return self.RESULT

    def get_offset(self) -> int:
        return self.OFFSET

    def set_result(self, new_RESULT: int):
        self.RESULT = new_RESULT - self.OFFSET

    def set_offset(self, new_OFFSET: int):
        self.OFFSET = new_OFFSET

    def set_gain(self, new_GAIN: int):
        '''
        :param new_GAIN: new GAIN 128 / 64 / 32
        '''
        match new_GAIN:
            case 128:
                self.GAIN = 1
            case 64:
                self.GAIN = 2
            case 32:
                self.GAIN = 3
            case _:
                raise ValueError("new_GAIN must be 128 / 64 / 32")            

def set_offset(hx711: HX711):
    hx711.set_offset(0)
    hx711.set_offset(read(hx711))

def is_ready(hx711: HX711) -> bool:
    return digitalRead(hx711.DOUT) == 0

def wait_ready(hx711: HX711, time: int):
    '''
    :param time: time in ms
    :type time: int
    '''
    while(not is_ready(hx711)): delay(time)

def shiftIn(dataPin: int, clockPin: int) -> int:

    value = 0

    for i in range(8):
        digitalWrite(clockPin, HIGH)
        value |= digitalRead(dataPin) << (7 - i)
        digitalWrite(clockPin, LOW)
        # Delay pre stabilizaciu
        # Bez toho moze citat falosne udaje
        delayMicros(1)

    return value

def read(hx711: HX711) -> int:
    wait_ready(hx711, 1)

    value = 0
    data = [0, 0, 0]

    with mux:
        for i in range(3):
            data[2 - i] = shiftIn(hx711.DOUT, hx711.SCK)

        for i in range(hx711.GAIN):
            digitalWrite(hx711.SCK, HIGH)
            delayMicros(1)
            digitalWrite(hx711.SCK, LOW)
            delayMicros(1)
    
    value = data[2] << 8*2 \
          | data[1] << 8   \
          | data[0]

    if value & 0x800000:
        value -= 0x1000000

    hx711.set_result(value)

    return value