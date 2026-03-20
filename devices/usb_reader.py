from device_module import DataReader
from status_codes import SUCCESS
from device_types import Device
from serial_reader import SerialReader

class USBSerialReader(SerialReader):
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        super().__init__(port=port, baudrate=baudrate)
        self.change_name(3)
    


if __name__ == '__main__':
    import os

    os.system('clear')

    print('Testing USB reader')

    reader = USBSerialReader()
    reader.connect()

    reader.read_data()

    print(reader.get_sys_logs())
    print(reader.get_readings_logs())

    print('Test passed')
