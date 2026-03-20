import serial
from time import sleep
from device_module import DataReader
from device_types import Device
from status_codes import SUCCESS, FAILED

class SerialReader(DataReader):

    def __init__(self, port='/dev/ttyAMA0', baudrate=9600):
        super().__init__()
        self.name = Device(1).get_device_name
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        
    
    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.sys_log(f'Connecting to {self.name} succeeded')
        except:
            self.sys_log(f'Connection to {self.name} failed')

    def read_data(self):
        try:
            if self.ser and self.ser.is_open:
                data = self.ser.readline().decode('utf-8').strip()
                self.log_reading(self.name, SUCCESS)
                return data
            else:
                self.sys_log(f'Connection to {self.name} is undefined')
                return None
        except:
            self.sys_log(f'Reading data from {self.name} failed')
            return None
        
    def disconnect(self):
        try:
            if self.ser:
                self.ser.close()
                self.sys_log(f'Disconnected from {self.name}')
        except:
            self.sys_log(f'Disconnection from {self.name} failed')
            

if __name__ == '__main__':

    print('Testing Serial connector\n')

    reader = SerialReader()
    assert reader.name == 'Serial', f'Incorrect device type'

    reader.connect()
    print(reader.get_sys_logs())
    
    reader.read_data()
    print(reader.get_sys_logs())

    
    

    print('Test passed\n')

    

