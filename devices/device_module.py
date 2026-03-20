from abc import  abstractmethod
from datetime import datetime
import os 


"""
TODO: Log the readings to persistent file system
Configure the system to start reading on boot up
"""

class DataReader:

    """Abstracct base class for all data readers"""

    def __init__(self):
        self.logs = []
        self.sys_logs = []
        self.tot_reads = 0
        self.failed_reads = 0
        self.connected = False 

    def is_connected(self):
        return self.connected


    def get_sys_logs(self):
        return self.sys_logs
    
    def get_readings_logs(self):
        return self.logs
    

    def log_reading(self, device, read_status):
        log_dict = {
            'time': datetime.now(), 
            'device': device, 
            'status': read_status 
        }
        self.logs.append(log_dict)

        if(read_status):
            self.tot_reads += 1
        
        else:
            self.failed_reads += 1

    def sys_log(self, msg=None):
        tot_reads  = self.tot_reads + self.failed_reads
        len_logs = len(self.logs)
        bool_mask = tot_reads == len_logs

        log_dict = {'time': datetime.now(), 'msg': msg, 'tot reads': tot_reads, 'tot_logs': len_logs}

        if not bool_mask:
            updated_msg = 'Incosistent dims of readings'
            log_dict['msg'] = updated_msg if msg == None else f'{msg}, {updated_msg}' 

        self.sys_logs.append(log_dict)
            

    @abstractmethod
    def connect(self):
        """Initialize connection to device"""
        raise NotImplementedError()
    
    @abstractmethod
    def read_data(self):
        """Read data from source"""
        raise NotImplementedError()
    
    @abstractmethod
    def disconnect(self):
        """Clean up connection"""
        raise NotImplementedError()
    


if __name__ == "__main__":

    print('Testing Device Reader Abstract class')

    data_reader = DataReader()
    assert len(data_reader.logs) == 0, f'Logs should be empty'
    assert len(data_reader.sys_logs) == 0, f'system logs should be empty'

    data_reader.log_reading('serial', True)
    assert len(data_reader.logs) == data_reader.tot_reads, f'Incosistent shape'


    data_reader.sys_log('Failed to connect to device')

    print(data_reader.sys_logs)

    print('Test passed\n')