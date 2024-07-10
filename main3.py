import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_connection():
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

def retrieve_data(connection):
    query = "SELECT timestamp, cpu_usage, nic_power FROM telemetry"
    df = pd.read_sql(query, connection)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def calculate_average_power(df):
    avg_cpu_usage = df['cpu_usage'].mean()
    avg_nic_power = df['nic_power'].mean()
    print(f"Average CPU Usage: {avg_cpu_usage:.2f}%")
    print(f"Average NIC Power: {avg_nic_power:.2f} W")

if __name__ == "__main__":
    db_connection = create_connection()
    if db_connection:
        data_df = retrieve_data(db_connection)
        calculate_average_power(data_df)
