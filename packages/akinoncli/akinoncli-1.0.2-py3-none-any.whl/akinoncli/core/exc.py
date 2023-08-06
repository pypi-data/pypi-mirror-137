from typing import Optional

import requests


class BaseAkinonCLIException(Exception):
    def __init__(self, message: str, *, response: Optional[requests.Response] = None):
        super().__init__(message, response)
        self.message = message
        self.response = response


class AkinonCLIError(BaseAkinonCLIException):
    """Generic errors."""
    ...


class AkinonCLIWarning(BaseAkinonCLIException):
    """Generic warnings."""
    ...
