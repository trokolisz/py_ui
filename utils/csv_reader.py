from pandas import read_csv
import sqlite3
from logger import ErrorLogger
from config_parser import get_data_csv_path, get_data_db_path

# Initialize the ErrorLogger with the name 'CSVReader'
error_logger = ErrorLogger(name='CSVReader')

# Get the file paths for the CSV and SQLite database from the configuration
csv_path = get_data_csv_path()
db_path = get_data_db_path()


class CSVReader:
    def __init__(self):
        # Dataframe to hold the CSV data
        self.df = None

    def read_csv(self, file_path: str = csv_path, DEBUG: bool = False):
        """
        Reads the CSV file from the given file path.
        
        Args:
         - file_path (str): Path to the CSV file
         - DEBUG (bool): If True, logs debug information
        
        Raises:
         - Logs error if file is not found or if any other error occurs during reading
        """
        try:
            if DEBUG:
                error_logger.log_debug(f'Reading csv file: {file_path}')
            self.df = read_csv(file_path)
        except FileNotFoundError:
            error_logger.log_error(f'File not found: {file_path}')
        except Exception as e:
            error_logger.log_error(f'Failed to read csv file: {file_path}. Error: {e}')
        except:
            error_logger.log_error(f'Failed to read csv file: {file_path}')

    def save_to_sqlite(self, db_path: str = db_path, table_name: str = 'data'):
        """
        Saves the read CSV data to an SQLite database.
        
        Args:
         - db_path (str): Path to the SQLite database file
         - table_name (str): Name of the table to save the data
        
        Raises:
         - Logs error if any error occurs during saving data to SQLite
        """
        try:
            conn = sqlite3.connect(db_path)
            self.df.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.close()
        except Exception as e:
            error_logger.log_error(f'Failed to save data to {db_path}. Error: {e}')
        except:
            error_logger.log_error(f'Failed to save data to {db_path}')

    def get_df(self):
        """
        Returns the DataFrame containing the CSV data.
        
        Returns:
         - DataFrame: The CSV data in DataFrame format
        """
        return self.df

if __name__ == '__main__':
    # Create an instance of CSVReader
    reader = CSVReader()
    # Read the CSV file and enable debug logging
    reader.read_csv('data.csv', DEBUG=True)
    # Save the read CSV data to SQLite database with table name 'data'
    reader.save_to_sqlite('data.db', 'data')
    # Print the DataFrame to console
    print(reader.get_df())