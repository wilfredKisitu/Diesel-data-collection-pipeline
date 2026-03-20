from pymodbus.client import ModbusSerialClient
from pymodbus.framer import FramerRTU
from device_module import DataReader
from device_types import Device
from status_codes import SUCCESS

class ModbusReader(DataReader):

    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        super().__init__()
        self.client = ModbusSerialClient(framer='rtu', port=port, baudrate=baudrate)
        self.name = Device(2).get_device_name

    
    def connect(self):
        ret = self.client.connect()
        if ret:
            self.sys_log(f'Connected to {self.name}')

        else:
            self.sys_log(f'Failed to connect to {self.name}')
            

    def read_data(self):
        try:
            result = self.client.read_holding_registers(0, 10)
            if result.isError():
                self.sys_log(f'Connection to {self.name} is undefined')
                return None
            
            self.log_reading(self.name, SUCCESS)
            result.registers
        except:
            self.sys_log(f'Reading data from {self.name} failed')
            return None
        

    def disconnect(self):
        try:
            self.client.close()
            self.sys_log(f'Closed connection to {self.name}')
        except:
            self.sys_log('Closing connection to {self.name} failed')


if __name__ == '__main__':
    import os
    os.system('clear')

    print('Testing modus connection module')

    reader = ModbusReader()
    assert reader.name == 'Modbus', f'Inconsistent name initition'
    reader.connect()
    print(reader.get_sys_logs())

    reader.connect()
    print(reader.get_sys_logs())



    print('Test passed')