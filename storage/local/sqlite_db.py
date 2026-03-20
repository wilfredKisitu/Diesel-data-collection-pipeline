import sqlite3
from typing import Any, List, Dict
from storage.db_interface import DatabaseInterface

class SQLiteDB(DatabaseInterface):

    def __init__(self, db_path: str):
        super().__init__()
        self.db_path = db_path
        self.conn: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None

    
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.dp_path)
            self.row_factory = sqlite3.Row  # enables dict-like rows
            self.cursor = self.conn.cursor()
        except:
            self.sys_logs()
    
    def disconnect(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None
            self.cursor = None
