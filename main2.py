
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
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

def visualize_data(df):
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(df['timestamp'], df['cpu_usage'], marker='o', linestyle='-')
    plt.xlabel('Timestamp')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage Over Time')
    plt.xticks(rotation=45)

    plt.subplot(2, 1, 2)
    plt.plot(df['timestamp'], df['nic_power'], marker='o', linestyle='-', color='red')
    plt.xlabel('Timestamp')
    plt.ylabel('NIC Power (W)')
    plt.title('NIC Power Over Time')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    db_connection = create_connection()
    if db_connection:
        data_df = retrieve_data(db_connection)
        visualize_data(data_df)
