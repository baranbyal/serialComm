import serial
import time
import threading

data1 = "ST,NT,0A,   "
input_data = "0.939"
data2 = "  g\r\n"

class SerialCommApp:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        try:
            self.ser = serial.Serial(port, baudrate)
        except serial.SerialException as e:
            print("Error opening serial port:", e)

    def send(self, data):
        self.ser.write(data.encode())

    def receive(self):
        if self.ser.in_waiting > 0:
            return self.ser.readline().decode()
        return None

    def close(self):
        self.ser.close()

def send_data(ser, lock):
    global input_data, data1, data2
    while True:
        lock.acquire()
        ser.send(data1 + input_data + data2)
        lock.release()
        time.sleep(0.1)

def receive_from_terminal(lock):
    global input_data
    while True:
        new_input = input("Enter the data to send: ")
        with lock:
            input_data = new_input

def receive_data(ser, lock):
    while True:
        lock.acquire()
        # print(ser.receive())
        received_data = ser.receive()
        if received_data:
            #print new line character
            print("\n")
            print(received_data)
            
            
        lock.release()
        time.sleep(1)

if __name__ == "__main__":
    ser = SerialCommApp("COM1", 9600)
    lock = threading.Lock()
    t1 = threading.Thread(target=send_data, args=(ser,lock))
    t2 = threading.Thread(target=receive_from_terminal, args=(lock,))
    t3 = threading.Thread(target=receive_data, args=(ser,lock))

    t1.start()
    t2.start()
    t3.start()