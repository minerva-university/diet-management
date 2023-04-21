import logging
from config import Config

logging.basicConfig(level=logging.DEBUG)

def setFormatter(fileName):
    #Creates a file handler with a formatter for logging
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(fileName)
    file_handler.setFormatter(formatter)

    return file_handler

# Setting up logger
info_logger = logging.getLogger(f"Diet_Manager_info")
info_logger.setLevel(logging.INFO)

# Setting up logger
error_logger = logging.getLogger(f"Diet_Manager_error")
error_logger.setLevel(logging.ERROR)

info_logger.info("Logging Running")

#Formatter 
fileFormatter = setFormatter(Config.LOG_FILE_NAME)
info_logger.addHandler(fileFormatter)
error_logger.addHandler(fileFormatter)
info_logger.addHandler(logging.StreamHandler())
error_logger.addHandler(logging.StreamHandler())

