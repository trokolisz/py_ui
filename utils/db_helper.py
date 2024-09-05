import sqlite3
import pandas as pd
from .config_parser import get_config_value
from .logger import ErrorLogger, changeLogger

class DBHelper:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.error_logger = ErrorLogger(name='DBHelper')
        self.change_logger = changeLogger(name='DBHelper')

    def create_db(self, table_name: str, columns: list) -> None:
        """Creates a new database with a table and columns."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join(columns[1:])})")
        conn.commit()
        conn.close()
        self.change_logger.log_info(f"Created table {table_name} with columns {columns}")

    def insert_data(self, table_name: str, data: list) -> None:
        """Inserts data into a table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executemany(f"INSERT INTO {table_name} ({', '.join(data[0].keys())}) VALUES ({', '.join(['?' for _ in range(len(data[0]))])})", [tuple(item.values()) for item in data])
        conn.commit()
        conn.close()
        self.change_logger.log_info(f"Inserted data into table {table_name}: {data}")

    def read_data(self, table_name: str) -> list:
        """Reads data from a table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        conn.close()
        return data

    def read_dataframe(self, table_name: str) -> pd.DataFrame:
        """Reads data from a table and returns it as a pandas DataFrame."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        conn.close()
        return df


    def update_data(self, table_name: str, data: list) -> None:
        """Updates data in a table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executemany(f"UPDATE {table_name} SET {', '.join([f'{key} = ?' for key in data[0].keys() if key != 'id'])} WHERE id = ?", [(tuple(item.values())[:-1] + (item['id'],)) for item in data])
        conn.commit()
        conn.close()
        self.change_logger.log_info(f"Updated data in table {table_name}: {data}")

    def delete_data(self, table_name: str, ids: list) -> None:
        """Deletes data from a table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executemany(f"DELETE FROM {table_name} WHERE id = ?", [(id,) for id in ids])
        conn.commit()
        conn.close()
        self.change_logger.log_info(f"Deleted data from table {table_name} with ids: {ids}")

    def table_exists(self, table_name: str) -> bool:
        """Checks if a table exists in a database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def delete_table(self, table_name: str) -> None:
        """Deletes a table from a database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE {table_name}")
        conn.commit()
        conn.close()
        self.change_logger.log_info(f"Deleted table {table_name}")

if __name__ == "__main__":
    csv_path = get_config_value('data_csv', 'path')
    db_path = get_config_value('data_db', 'path')
    db_helper = DBHelper(db_path)

    # Create a new database
    if db_helper.table_exists("data"):
        db_helper.delete_table("data")
    db_helper.create_db("data", ["id", "name", "age", "gender", "city", "state", "country", "zip_code", "email", "phone_number"])

    # Insert data into the database
    data = [
        {"name": "John Doe", "age": 25, "gender": "Male", "city": "New York", "state": "NY", "country": "USA", "zip_code": "10001", "email": "john@example.com", "phone_number": "123-456-7890"},
        {"name": "Jane Smith", "age": 30, "gender": "Female", "city": "Los Angeles", "state": "CA", "country": "USA", "zip_code": "90210", "email": "jane@example.com", "phone_number": "987-654-3210"},
        {"name": "Bob Johnson", "age": 35, "gender": "Male", "city": "Chicago", "state": "IL", "country": "USA", "zip_code": "60601", "email": "bob@example.com", "phone_number": "555-555-5555"},
        {"name": "Alice Brown", "age": 28, "gender": "Female", "city": "San Francisco", "state": "CA", "country": "USA", "zip_code": "94105", "email": "alice@example.com", "phone_number": "555-555-5555"},
        {"name": "David Lee", "age": 40, "gender": "Male", "city": "New York", "state": "NY", "country": "USA", "zip_code": "10001", "email": "david@example.com", "phone_number": "555-555-5555"}
    ]
    db_helper.insert_data("data", data)

    # Read data from the database
    data = db_helper.read_data("data")
    print(data)

    # Read data from the database as a pandas DataFrame
    df = db_helper.read_dataframe("data")
    print(df)

    # Update data in the database
    db_helper.update_data("data", [{"id": 1, "name": "Johnathan Doe", "age": 26, "gender": "Male", "city": "New York", "state": "NY", "country": "USA", "zip_code": "10001", "email": "johnathan@example.com", "phone_number": "123-456-7890"}])

    # Delete data from the database
    db_helper.delete_data("data", [1])
