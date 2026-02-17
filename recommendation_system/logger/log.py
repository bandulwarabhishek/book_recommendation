import logging 
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_DIR = os.path.join(os.getcwd(), LOG_DIR)   # type: ignore
#getcwd() returns the current working directory(from where your script is running)
# os.path.join() joins the path safely with correct path separator


#Creating LOG_DIR if it does not exist
os.makedirs(LOG_DIR, exist_ok=True)
#exist_ok=True means if the directory exists, it  won't do anything, if folder does not exist, it will create a new.


#Creating file name for log file based on current timestamp
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
file_name = f"log_{CURRENT_TIME_STAMP}.log"


#Creating file path for log file
log_file_path = os.path.join(LOG_DIR, file_name)


#Setting up logging configuration
logging.basicConfig(
    filename=log_file_path,  #all logs messages will be written to this file
    format="[%(asctime)s %(name)s - %(levelname)s - %(message)s]", #log message format, it includes timestamp, logger name, log level and the actual log message
    level=logging.NOTSET 
)