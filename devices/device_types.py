from enum import Enum

class Device(Enum):
    SERIAL = 1
    MODBUS = 2
    FUTURE_PROTOCOLS = 3
    UNKNOWN = 0

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

    @property
    def get_device_name(self):
        mapping = {
            Device.SERIAL: 'Serial',
            Device.MODBUS: 'Modbus',
            Device.FUTURE_PROTOCOLS: 'Futue protocols',
            Device.UNKNOWN: 'Unsupported protocol'
        }
        return mapping.get(self)

        


if __name__ == '__main__':
    print('Testing Device types')

    protocol = Device(5)
    print(protocol.get_device_name)

    print('Test passed')



