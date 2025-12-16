import threading
import os
from HX711 import *

GPIO.setmode(GPIO.BCM)

PIN_COUNT = 5
DOUT_PINS = []
SCK_PINS  = []
RESULT    = [''] * PIN_COUNT

hx711 = []

even_done = threading.Event()
odd_done = threading.Event()

def task_even():
    global RESULT
    while True:
        for i in range(0, PIN_COUNT, 2):
            RESULT[i] = str(read(hx711[i]))
        even_done.set()
        delayMicros(1)
        even_done.clear()

def task_odd():
    global RESULT
    while True:
        for i in range(1, PIN_COUNT, 2):
            RESULT[i] = str(read(hx711[i]))
        odd_done.set()
        delayMicros(1)
        odd_done.clear()

def result_to_string() -> str:
    result = ''
    for i in range(PIN_COUNT):
        result += str(RESULT[i] + ';')
    result += '\n'

    return result

if __name__ == "__main__":
    for i in range(PIN_COUNT):
        hx711.append(HX711(DOUT_PINS[i], SCK_PINS[i]))

    even_thread = threading.Thread(target=task_even)
    odd_thread  = threading.Thread(target=task_odd)
    
    fifo_path = "./fifo_file"
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)

    with open(fifo_path, 'w') as fifo:
        while True:
            even_done.wait()
            odd_done.wait()

            fifo.write(result_to_string())
            fifo.flush()
            delayMicros(10)

