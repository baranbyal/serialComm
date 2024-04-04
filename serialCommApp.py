# #Send the data to the serial port
# # In this project, I will send the serial data "ST,NT,0À,   0.939  g" to the COM12 port in each 100ms. The serial data array will 20bytes with data and the additional 2 bytes for '/r/n'. 
# # while doing this, also print the received data from the serial port.

# # give me a chance to change the 0.939 to a valure that I want to send.
# # I may want to type the value that I want to send in the console.



# import serial
# import time
# import threading

# # Serial Communication Application
# # 
# data1 = "ST,NT,0A,   "
# data2 = "  g\r\n"
# input_data = "0.939"

# class SerialCommApp:
#     def __init__(self, port, baudrate):
#         self.port = port
#         self.baudrate = baudrate
#         self.ser = serial.Serial(port, baudrate)

#     def send(self, data):
#         self.ser.write(data.encode())

#     def receive(self):
#         return self.ser.readline().decode()

#     def close(self):
#         self.ser.close()

# def send_data(ser):
#     while True:
#         # ser.send(data)
#         # ser.send("ST,NT,0A,   0.939  g\r\n")
#         ser.send(data1 + input_data + data2)
#         # print(ser.receive())
#         time.sleep(0.1)

# def receive_from_terminal():
#     new_input = input("Enter the data to send: ")
#     input_data = new_input


# # create a thread for sending the data
# # create a thread for receiving the data from the terminal

# if __name__ == "__main__":
#     ser = SerialCommApp("COM14", 9600)
#     t1 = threading.Thread(target=send_data, args=(ser,))
#     t2 = threading.Thread(target=receive_from_terminal)

#     #give t2 the highest priority

#     t1.start()
#     t2.start()

import serial
import time
import threading
from queue import Queue

# Serial Communication Application

data1 = "ST,NT,0A,   "
data2 = "  g\r\n"

class SerialCommApp:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)

    def send(self, data):
        self.ser.write(data.encode())

    def receive(self):
        return self.ser.readline().decode()

    def close(self):
        self.ser.close()

def send_data(ser, input_queue):
    while True:
        # Check if there's any user input
        if not input_queue.empty():
            # input_data = input_queue.front()
            #get the first element from the queue
            input_data = input_queue.get()
            input_queue.put(input_data)

            ser.send(data1 + input_data + data2)
        else:
            ser.send(data1 + "0.939" + data2)  # Default value
        time.sleep(0.1)

def receive_from_terminal(input_queue):
    while True:
        new_input = input("Enter the data to send: ")
        input_queue.put(new_input)

def queue_handler(input_queue):
    while True:
        #if the queue size is greater than 1
        if input_queue.qsize() > 1:
            input_queue.get()

if __name__ == "__main__":
    ser = SerialCommApp("COM14", 9600)
    input_queue = Queue()

    t1 = threading.Thread(target=send_data, args=(ser, input_queue))
    t2 = threading.Thread(target=receive_from_terminal, args=(input_queue,))
    t3 = threading.Thread(target=queue_handler, args=(input_queue,))

    #if keykoard interrupt is pressed, close the serial port

    t1.start()
    t2.start()
    t3.start()
