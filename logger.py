import logging
import os

def setup_logger(log_file, log_level=logging.INFO, console_output=False):
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a logger
    logger = logging.getLogger('StatusMonitor')
    logger.setLevel(log_level)

    # Create a file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create a formatting configuration
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    
    if console_output:
        logger.addHandler(console_handler)
        

    return logger
