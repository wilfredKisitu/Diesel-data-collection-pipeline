import psycopg2
from typing import Any, List, Dict
from storage.db_interface import DatabaseInterface



class NeonDB(DatabaseInterface):

    def __init__(self, connection_url: str):
        super().__init__()
        self.connection_url = connection_url
        self.conn =  None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(self.connection_url)
            self.cursor = self.conn.cursor()
            self.log_to_sys(f'Connected to Neon DB')
        except Exception as conn_err:
            self.log_to_sys(f'Failed to connected to Noen database {conn_err}')

    def disconnect(self):
        try:
            if self.conn:
                self.conn.commit()
                self.conn.close()
                self.log_to_sys('Disconnected from Neon Database')
        except Exception as discon_error:
            self.log_to_sys('Failed to disconnect from Neon Database')

    def insert(self, table: str,  data: Dict[str, Any]):
        try:
            keys = ', '.join(data.keys())
            placeholders = ', '.join(["%s"]*len(data))
            values = tuple(data.values())

            sql = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
            self.cursor.execute(sql, values)
            self.conn.commit()
            self.log_to_sys(f'Inserted into {table} in Neon DB')

        except Exception as insert_err:
            self.conn.rollback()
            self.log_to_sys(f'Failed to insert into {table} in Neon DB {insert_err}')

    def update(self, table: str, data:Dict[str, Any], where: Dict[str, Any]):
        try:
            set_clause = ', '.join([f"{k}=%s" for k in data.keys()])
            where_clause = " AND ".join([f"{k}=%s" for k in where.keys()])

            values = tuple(data.values()) + tuple(where.values())
            sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            self.cursor.execute(sql, values)
            self.conn.commit()
            self.log_to_sys(f'Updated {table} in Neon Database')
        except Exception as update_err:
            self.conn.rollback()
            self.log_to_sys(f'Failed to update {table} in Neon DB {update_err}')

    
    def read(self, table, columns = None, where = None):
        try:
            cols = ', '.join(columns) if columns else '*'
            sql = f"SELECT {cols} FROM {table}"
            values = ()

            if where:
                where_clause = ' AND '.join([f"{k}=%s" for k in where.keys()])
                sql += f" WHERE {where_clause}"
                values = tuple(where.values())
            
            self.cursor.execute(sql, values)
            rows = self.cursor.fetchall()

            self.log_to_sys(f'Read data from {table} from Neon DB')

            return rows
        except Exception as read_err:
            self.log_to_sys(f'Failed to read data from {table} from Neon DB {read_err}')

if __name__ == '__main__':

    from storage.cloud.neon_db import NeonDB
    from dotenv import load_dotenv
    from datetime import datetime
    import os

    print('Testing cloud database')

    load_dotenv('.env.local')
    database_url = os.getenv("DATABASE_URL")
    
    db = NeonDB(database_url)
    db.connect()

    db.cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS engine_data(
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                rpm INTEGER,
                temperature REAL,
                fuel_level REAL
            )
        """
    )
    db.conn.commit()

    db.insert("engine_data", {
        "timestamp": datetime.now(),
        "rpm": 1500,
        "temperature": 1500,
        "fuel_level": 50.2
    })

    print('\n Before Updating')
    print(db.read('engine_data'))

    db.update(
        table="engine_data",
        data= {"rpm": 1800, "temperature": 95.0},
        where={"id": 1}
    )

    print("\n After update")
    print(db.read('engine_data'))

    print(db.get_sys_logs())

    db.disconnect()

    print('Test passed')