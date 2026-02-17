from recommendation_system.logger.log import logging
from recommendation_system.exception.exception_handler import AppException
import sys



logging.info("Starting the application...")

try:
    a=1/0
except Exception as e:
    raise AppException(e,sys)