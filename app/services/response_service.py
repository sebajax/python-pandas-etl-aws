"""
global response service for all the use cases
"""

from typing import Union

from pydantic import BaseModel


class ResponseService(BaseModel):
    """ class to represent the services exception to return to  presentation layer """
    detail: str
    data: Union[dict, None] = None
