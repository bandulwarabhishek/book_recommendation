# import os
import sys

class AppException(Exception):

    # AppException is a cutomized exception class designed to capture refined details about Exception
    # such as python script file line number along with error message with a custom exception one can easily spot source of error and 
    # provide quick fix.

    def __init__(self, error_message: Exception, error_detail: sys): # type: ignore
        # param error_message: error message in string format

        super().__init__(error_message)
        self.error_message = AppException.error_message_detail(error_message, error_detail=error_detail)

    @staticmethod
    def error_message_detail(error:Exception, error_detail:sys): #type: ignore
        """
        error: Exception object raise from module
        error_details: is sys module contains detail information about system execution information.
        """

        _, _, exc_tb = error_detail.exc_info()
        #extracting file name from exception traceback
        file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "File is Unknown"

        #preparing error message
        line_number = exc_tb.tb_lineno if exc_tb else "Line number is Unknown"
        error_message = f"Error occured in script: [{file_name}] at line number: [{line_number}] error message: [{error}]"

        return error_message
    
    def __repr__(self):
        #Formatting object of AppException

        return AppException.__name__.__str__()
    
    def __str__(self):
        #Formatting how a object should be visible if used in print statement

        return self.error_message
