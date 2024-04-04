# Now I want to create a web application that will allow me to send the data to the serial port.
# One way to do this is to use Flask.
# I will have a text box where I can enter the data that I want to send.
# One parameter that controls the period of sending the data.
# There will be a text box where it show the data that is received from the serial port.
# One parameter that controls the COM port.
# Do it with OOP
# the page should be dynamic and should not require a refresh.



from flask import Flask, render_template, request
from serial import Serial
import threading
import time

app = Flask(__name__)

class SerialCommApp:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.serial_port = Serial(port, baudrate)
        self.lock = threading.Lock()
        self.input_data = "test"
        self.received_data = ""
        self.interval = 0.1

    def send(self):
        self.lock.acquire()
        data = self.input_data + "\r\n"
        self.lock.release()
        self.serial_port.write(data.encode())

    # def receive(self):
    #     if self.serial_port.in_waiting > 0:
    #         with self.lock:
    #             self.received_data = self.serial_port.readline().decode().strip()

    def setSendData(self, data):
        self.input_data = data

    def getSendData(self):
        return self.input_data
    
    def setInterval(self, interval):
        self.interval = interval

    def getInterval(self):
        return self.interval

    def close(self):
        self.serial_port.close()

ser = None  # Initialize ser outside of the route function
t1 = None


def send_data_obj(ser):
    while True:

        if ser:
            ser.send()
            time.sleep(ser.getInterval())

# def receive_data(ser):
#     while True:
#         if ser:
#             ser.receive()
#         time.sleep(0.1)  # Adjust as needed based on the data rate

@app.route('/', methods=['GET', 'POST'])
def index():
    global ser
    
    return render_template('index.html')

@app.route('/send_data', methods=['POST'])
def send_data():
    global ser
    if request.method == 'POST':
        data_to_send = request.form['data_to_send']

        interval = float(request.form['interval']) / 1000
        
        if ser:
            print("Com port:", ser.port)
            print("Baud rate:", ser.baudrate)
            
            print("Data to send:", data_to_send)
            ser.setSendData(data_to_send)
            ser.setInterval(interval)
        else:
            print("Serial port not initialized")
    return render_template('index.html')
    
@app.route('/create_connection', methods=['POST'])
def create_connection():
    global ser
    global t1
    if request.method == 'POST':
        port = request.form['serial_port']
        baudrate = int(request.form['baud_rate'])
        if ser:
            ser.close()
            ser = None
        if t1:
            t1.join()
        try:
            ser = SerialCommApp(port, baudrate)
            print("Serial port opened successfully")
            t1 = threading.Thread(target=send_data_obj, args=(ser,))
            # t2 = threading.Thread(target=receive_data, args=(ser,))
            print("Threads created")
            t1.start()
            # t2.start()
        except Exception as e:
            # send the error message to the frontend as a flash message
            print("Error opening serial port:", e)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

