import serial
from time import sleep
from datetime import datetime
from devices.device_module import DataReader

class SerialReader(DataReader):

    def __init(self, port='/dev/ttyAMA0', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = None


    
    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f'Connected to Serial on {self.port}')
        except:
            raise ValueError(f'Failed to connect to port {self.port}')
        

    def read_data(self):
        try:
            if self.ser and self.ser.is_open:
                data = self.ser.readline().decode('utf-8').strip()
                return data
        except:
            pass
            

    

