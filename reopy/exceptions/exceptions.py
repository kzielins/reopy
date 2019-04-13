#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

class LogInException(Exception):
    """
    Raised if one cannot log into the specified, e.g. because the password is wrong
    """

    def __init__(self, msg: str = "Login failed"):
        super().__init__(msg)
        self._msg = msg

    def __repr__(self):
        return f'{self._msg}'


class CameraError(Exception):
    """
    Raised if the specified camera is unable to process the provided JSON data
    """

    def __init__(self, msg: str = "An error occurred while trying to process the request"):
        super().__init__(msg)
        self._msg = msg

    def __repr__(self):
        return f'{self._msg}'
