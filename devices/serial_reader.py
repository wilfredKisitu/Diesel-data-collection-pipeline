import serial
from time import sleep
from device_module import DataReader
from device_types import Device

class SerialReader(DataReader):

    def __init__(self, port='/dev/ttyAMA0', baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.name = Device(1).get_device_name
    
    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.log_reading()
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
            

if __name__ == '__main__':
    import os
    os.system('clear')

    print('Testing Serial connector\n')

    reader = SerialReader()
    assert reader.name == 'Serial', f'Incorrect device type'

    print('Test passed\n')

    

