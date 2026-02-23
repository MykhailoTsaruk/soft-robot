import os
import time

PIN_COUNT = 1
DATA_SAMPLE = 10

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

if __name__ == "__main__":
    fifo_path = "./fifo_file"
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)

    with open(fifo_path, 'r') as fifo:
        print("Fifo open successfull")
        
        counter = 0

        data_list = [[0] * DATA_SAMPLE for _ in range(PIN_COUNT)]
        
        start_time = time.perf_counter()

        while True:
            data = fifo.readline()
            if data == '':
                time.sleep(1 / 1000)
                continue

            new_data = data.split(';')[0:-1]

            for i in range(len(new_data)):
                data_list[i][counter] = int(int(new_data[i]) / 1000)
            
            # print(data_list)

            if counter < DATA_SAMPLE-1:
                counter += 1
            else:
                filtered_data = data_filter(data_list)
                counter = 0
                print(filtered_data)            
                end_time = time.perf_counter()
                print(f"Cycle time: {(end_time-start_time):.3f}")
    
                start_time = time.perf_counter()

                



