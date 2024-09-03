import configparser
from logger import ErrorLogger

error_logger = ErrorLogger(name='ConfigParser')

def get_data_csv_path():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('Paths', 'data_csv', fallback='data/data.csv')
    except Exception as e:
        error_logger.log_error(f'Error: {e}')
        return 'data/data.csv'

def get_data_db_path():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('Paths', 'data_db')
    except Exception as e:
        error_logger.log_error(f'Error: {e}')
        return 'data/data.db'