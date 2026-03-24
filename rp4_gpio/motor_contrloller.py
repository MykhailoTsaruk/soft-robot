import os
import time
from motor import *
from enums import *

DEVICENAME              = 'COM3'
PROTOCOL_VERSION        = 2.0
BAUDRATE                = 57600

PIN_COUNT = 9
DATA_SAMPLE = 10

data_list = [[0] * DATA_SAMPLE for _ in range(PIN_COUNT)]
filtered_data = []
motors : list[Motor] = []


def data_filter(data_list) -> list:
    filtered_data = [0] * PIN_COUNT

    for i in range(PIN_COUNT):
        temp_list = data_list[i][:]
        count_of_remove = int(int(len(temp_list) * 0.4) / 2)
        for _ in range(count_of_remove):
            temp_list.remove(max(temp_list))
            temp_list.remove(min(temp_list))
        
        filtered_data[i] = int(sum(temp_list) / len(temp_list))

    return filtered_data

def data_reader():
    data = fifo.readline()
    if data == '':
        time.sleep(1 / 1000)
        return

    new_data = data.split(';')[0:-1]

    for i in range(len(new_data)):
        data_list[i][counter] = int(int(new_data[i]) / 1000)
    
def open_port():
    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        quit()

    return portHandler, packetHandler

if __name__ == "__main__":
    fifo_path = "./fifo_file"
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)

    with open(fifo_path, 'r') as fifo:
        print("Fifo open successfull")
        
        counter = 0

        portHandler, packetHandler = open_port()        

        for i in range(1, 10, 1):
            motors.append(Motor(i, packetHandler, portHandler))
        
        for motor in motors:
            motor.set_control_mode_velocity()

        # start_time = time.perf_counter()

        while True:

            if counter < DATA_SAMPLE-1:
                counter += 1
            else:
                filtered_data = data_filter(data_list)
                counter = 0
                print(filtered_data)            
                # end_time = time.perf_counter()
                # print(f"Cycle time: {(end_time-start_time):.3f}")
    
                # start_time = time.perf_counter()

            for i in range(0, 9, 3):
                if filtered_data[i] < 100:
                    motors[i].move_use_velocity(Direction.CW)
                else:
                    motors[i].move_use_velocity(-1)

            
            


                



