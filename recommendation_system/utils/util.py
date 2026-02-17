import yaml
# import os
from recommendation_system.exception.exception_handler import AppException


def read_yaml_file(file_path:str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the YAML file.
    """
    try:
        with open(file_path, 'rb') as file:
            content = yaml.safe_load(file)
        return content
    except Exception as e:
        raise AppException(e, sys) from e