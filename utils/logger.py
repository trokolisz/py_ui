import logging
import time


class ErrorLogger:
    def __init__(self, log_file: str='logs/error.log', name: str = "ErrorLogger") -> None:
        
        level: int=logging.DEBUG

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        
        # Stream handler (console)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        
        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
    
    def log_debug(self, message: str) -> None:
        self.logger.debug(message)
    
    def log_info(self, message: str) -> None:
        self.logger.info(message)
    
    def log_warning(self, message: str) -> None:
        self.logger.warning(message)
    
    def log_error(self, message: str) -> None:
        self.logger.error(message)
    
    def log_critical(self, message: str) -> None:
        self.logger.critical(message)


if __name__ == '__main__':
    error_logger = ErrorLogger(name='TestLogger')
    error_logger.log_debug('This is a debug message')
    error_logger.log_info('This is an info message')
    error_logger.log_warning('This is a warning message')
    error_logger.log_error('This is an error message')
    error_logger.log_critical('This is a critical message')