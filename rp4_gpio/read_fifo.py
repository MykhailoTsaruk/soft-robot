import os

if __name__ == "__main__":
    fifo_path = "./fifo_file"
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)

    with open(fifo_path, 'r') as fifo:
        while True:
            data = fifo.readline()
            if data == '':
                continue

            new_data = data.split(';')[0:-1]
            print(new_data)
