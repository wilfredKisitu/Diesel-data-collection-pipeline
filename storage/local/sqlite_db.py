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
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # enables dict-like rows
            self.cursor = self.conn.cursor()
            self.log_to_sys(f'Connected to {self.db_path}')
        except Exception as conn_err:
            self.log_to_sys(f'Failed to connect to {self.db_path}: {conn_err}')    
    def disconnect(self):
        try:
            if self.conn:
                self.conn.commit()
                self.conn.close()
                self.conn = None
                self.cursor = None
                self.log_to_sys(f'Disconnect from {self.db_path}')

        except Exception as disconn_err:
            self.log_to_sys(f'Failed to disconnect from {self.db_path}: {disconn_err}')

    
    def insert(self, table: str, data: Dict[str, Any]):
        try:
            keys = ','.join(data.keys())
            placeholders = ','.join(['?']* len(data))
            values = tuple(data.values())
            sql = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
            self.cursor.execute(sql, values)
            self.conn.commit()
            self.log_to_sys(f'Inserted data into {table} for {self.db_path}')

        except Exception as insert_err:
            self.log_to_sys(f'Failed to insert data into {self.db_path}')

    
    def update(self, table: str, data: Dict[str, Any], where: Dict[str, Any]):
        try:
            set_clause = ','.join([f'{k}=?' for k in data.keys()])
            where_clause = ' AND '.join([f'{k}=?' for k in where.keys()])
            values = tuple(data.values()) + tuple(where.values())
            sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            self.cursor.execute(sql, values)
            self.conn.commit()
            self.log_to_sys(f'Updated data {table} for {self.db_path}')

        except Exception as update_err:
            self.log_to_sys(f'Failed to update {table} for {self.db_path}')

    def read(self, table:str, columns: List[str]=None, where: Dict[str, Any]=None) ->List[Dict[str, Any]]:
        try:
            cols = ','.join(columns) if columns else "*"
            sql = f'SELECT {cols} FROM {table}'
            values = ()
            if where:
                where_clause = ' AND '.join([f'{k}=?' for k in where.keys()])
                sql += f" WHERE {where_clause}"
                values = tuple(where.values())
            self.cursor.execute(sql, values)
            rows = self.cursor.fetchall()
            self.log_to_sys(f'Read data from {table} for {self.db_path}')
            return [dict(row) for row in rows]
            
        except Exception as read_err:
            self.log_to_sys(f'Failed to read data from {table} for {self.db_path}')
            return None
        

if __name__ == '__main__':

    from storage.local.sqlite_db import SQLiteDB
    print('Testing Local storage')

    db= SQLiteDB('DB/diesel_data.db')
    db.connect()

    db.cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS engine_data(
                timestamp TEXT,
                rpm INTEGER,
                temperature REAL,
                fuel_level REAL
            )
        """
    )
    db.conn.commit()
    
    # insert a record
    db.insert('engine_data', {
        'timestamp': '2026-03-20 12:00:00',
        'rpm': 1200,
        'temperature': 85.5,
        'fuel_level': 50.2
    })

    print('Before update\n')
    rows_before = db.read('engine_data')
    print(rows_before)

    db.update(table='engine_data', data={'rpm': 1500, 'temperature':90.0}, where={'timestamp': '2026-03-20 12:00:00'})

    print('\nAfter update')
    rows_after = db.read('engine_data')
    print(rows_after)

    db.disconnect()

    # print(db.get_sys_logs())

    print('Test passed')
    
