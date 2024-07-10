import psutil
import time
import mysql.connector
from mysql.connector import Error

def create_connection():
    """ Create a database connection to the MySQL database """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='power_telemetry',
            user='root',
            password='captain'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

def collect_cpu_usage():
    return psutil.cpu_percent(interval=1)

def collect_nic_power():
    net_io = psutil.net_io_counters(pernic=True)
    if 'eth0' in net_io:
        return net_io['eth0'].power if hasattr(net_io['eth0'], 'power') else None
    return None

def insert_data(connection, timestamp, cpu_usage, nic_power):
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO telemetry (timestamp, cpu_usage, nic_power)
                      VALUES (%s, %s, %s)''', (timestamp, cpu_usage, nic_power))
    connection.commit()

def collect_and_insert_data(connection):
    try:
        while True:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            cpu_usage = collect_cpu_usage()
            nic_power = collect_nic_power()
            if nic_power is not None: 
                insert_data(connection, timestamp, cpu_usage, nic_power)
            time.sleep(4)  
    except KeyboardInterrupt:
        print("Data collection stopped by user.")
    finally:
        connection.close()

if __name__ == "__main__":
    db_connection = create_connection()
    if db_connection:
        collect_and_insert_data(db_connection)
