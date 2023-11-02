"""
global exception service for all the use cases
"""

from dataclasses import dataclass


@dataclass
class ServiceException(Exception):
    """ class to represent the services exception to return to  presentation layer """
    detail: str
