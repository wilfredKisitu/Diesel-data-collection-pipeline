from pymodbus.client import ModbusSerialClient
from devices.device_module import DataReader
from devices.status_codes import SUCCESS
from devices.device_types import Device


class USBModbusReader(DataReader):

    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, slave_id=1):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.slave_id = slave_id
        self.client = None
        self.name = Device(3).get_device_name

    def connect(self):
        self.client = ModbusSerialClient(framer='rtu', port=self.port, baudrate=self.baudrate, timeout=1)

        ret = self.client.connect()
        if ret:
            self.sys_log(f'Connected to {self.name} via {self.port}')
            self.connected = True


        else:
            self.sys_log(f'Connection to {self.name} failed')


    def read_data(self):
        result = self.client.read_holding_registers(0, count=10, device_id=self.slave_id)

        try:
            if result.isError():
                self.sys_log(f'Connection to {self.name} is undefined')
                return None
            else:
                self.log_reading(self.name, SUCCESS)
                return result.registers
        except:
            self.sys_log(f'Reading from {self.name} failed')
            return  None
    

    def disconnect(self):
        try:
            if self.client:
                self.client.close()
                self.sys_log(f'Closed {self.name}')
        except:
            self.sys_log(f'Failed to close {self.name}')


if __name__ == '__main__':
    print('Testing USB Modus Reader')

    reader = USBModbusReader()
    reader.connect()
    print(reader.is_connected())

    reader.read_data()

    print(reader.get_sys_logs())
    print(reader.is_connected())

    print('Test passed')

