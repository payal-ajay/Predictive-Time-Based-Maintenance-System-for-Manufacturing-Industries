import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import get_db_connection

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS machine_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            footfall FLOAT,
            tempMode FLOAT,
            AQ FLOAT,
            USS FLOAT,
            CS FLOAT,
            VOC FLOAT,
            RP FLOAT,
            IP FLOAT,
            Temperature FLOAT,
            fail INT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()