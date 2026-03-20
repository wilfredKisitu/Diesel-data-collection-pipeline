from abc import ABC, abstractmethod
from typing import Any, List, Dict
from datetime import datetime


class DatabaseInterface:

    def __init__(self):
        self.sys_logs = []
    
    def get_sys_logs(self):
        return self.sys_logs
    
    def log_to_sys(self, msg):
        msg_dict = {'time': datetime.now(), 'msg': msg}
        self.sys_logs.append(msg_dict)

    @abstractmethod
    def connect(self):
        """Connect to database"""
        raise NotImplementedError()
    
    @abstractmethod
    def disconnect(self):
        """Disconnect from the database"""
        raise NotImplementedError()
    

    @abstractmethod
    def insert(self, table: str, data: Dict[str, Any]):
        """Insert a record into a table"""
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, table: str, data: Dict[str, Any], where: Dict[str, Any]) ->List[Dict[str, Any]]:
        """Update records in a table matching the 'where' condition"""
        raise NotImplementedError()
    
    @abstractmethod
    def read(self, table: str, columns: List[str]= None, where: Dict[str, Any]=None) -> List[Dict[str, Any]]:
        """Read data from a table with optional filtering"""
        raise NotImplementedError()

if __name__== '__main__':
    print('Testing database interface')

    db_interface = DatabaseInterface()

    db_interface.log_to_sys('Testing if logging works')

    print(db_interface.get_sys_logs())

    print('Test passed')