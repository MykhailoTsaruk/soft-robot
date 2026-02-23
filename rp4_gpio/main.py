import os
import threading
import json

from HX711 import *
from sshkeyboard import listen_keyboard

# DOUT_PINS = [21, 20, 16, 12, 7]
# SCK_PINS  = [26, 19, 13,  6,  5]
DOUT_PINS = [21]
SCK_PINS  = [26]
PIN_COUNT = len(SCK_PINS)
RESULT    = [''] * PIN_COUNT

global OFFSET_SETTING
OFFSET_SETTING = False

hx711 = []
offset_path = './offset.json'

def result_to_string() -> str:
    result = ''
    for i in range(PIN_COUNT):
        result += str(RESULT[i] + ';')
    result += '\n'

    return result

def save_offset():
    offset = {}

    for i in range(PIN_COUNT):
        offset[f'{i}'] = hx711[i].get_offset()

    with open(offset_path, 'w') as f:
        json.dump(offset, f, indent=4)

def load_offset():
    offset = {}
    
    if os.path.exists(offset_path):
        with open(offset_path, 'r') as f:
            offset = json.load(f)
    else:
        print(f"File {offset_path} not exist")

    for i in range(len(offset)):
        hx711[i].set_offset(offset[f"{i}"])

def press(key):
    global OFFSET_SETTING
    match key:
        # Set and Save offset
        case 's':
            if OFFSET_SETTING == False:
                OFFSET_SETTING = True

        # Load offset
        case 'd':
            if OFFSET_SETTING == False:
                OFFSET_SETTING = True
                load_offset()
                print("Offset load")
                OFFSET_SETTING = False

        # Clear offset
        case 'o':
            if OFFSET_SETTING == False:
                OFFSET_SETTING = True
                for i in range(PIN_COUNT):
                    hx711[i].OFFSET = 0
                print("Offset clear")
                OFFSET_SETTING = False

def release(key):
    pass



def key_listener():
    listen_keyboard(
        on_press=press,
        on_release=release,
    )

listener_thread = threading.Thread(target=key_listener, name="Key-Listener", daemon=True)

if __name__ == "__main__":
    for i in range(PIN_COUNT):
        hx711.append(HX711(DOUT_PINS[i], SCK_PINS[i]))

    load_offset()
    print("Offset load")

    fifo_path = "./fifo_file"
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)

    with open(fifo_path, 'w') as fifo:
        print("Fifo open successfull")                

        listener_thread.start()

        while True:
            if OFFSET_SETTING == False:
                # start_time = Time.perf_counter()
                for i in range(PIN_COUNT):
                    read(hx711[i])
                    RESULT[i] = str(hx711[i].RESULT)

                fifo.write(result_to_string())
                fifo.flush()
                delay(1)

                # end_time = Time.perf_counter()
                # print(f"Cycle time: {(end_time-start_time):.3f}")
                
            else:
                for i in range(PIN_COUNT): 
                    set_offset(hx711[i])
                    save_offset()         
                    print("Offset set")   
                    OFFSET_SETTING = False

