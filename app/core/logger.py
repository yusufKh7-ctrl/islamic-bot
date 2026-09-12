import logging
import os

def setup_logger(name=__name__, log_file='app.log'):
    # Create Logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Avoid repeating message if the func is called more than onec
    if logger.hasHandlers():
        return logger

    # Format
    log_format = '%(asctime)s | %(levelname)s | %(message)s'
    date_format = '%Y-%m-%d | %H:%M:%S'
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
    


    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    is_render = os.getenv("RENDER") is not None
    if not is_render:
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, log_file)
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger