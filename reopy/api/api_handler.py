#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import sys
import time

import requests
import ujson

from reopy.exceptions import exceptions

class BasicAPIHandler:
    """
    A very basic interface used to interact with the undocumented
    Reolink camera API
    """

    def __init__(self, ip_address, password: str, username: str = "admin"):
        self._ip_address = ip_address

        self._password = password
        self._username = username

        self._token = ""
        self._lease_time = 0
        self._login_time = 0

        self._api_url = ""

    @property
    def token(self):
        """
        Token getter
        """

        return self._token

    def login(self):
        """
        Log into Reolink camera interface using the API
        """

        login_url = "http://{0}/cgi-bin/api.cgi?cmd=Login&token=null".format(self._ip_address)

        # Move to API Requests class?

        login_data = [
            {
                "cmd": "Login",
                "action": 0,
                "param": {
                    "User": {
                        "userName": "{}".format(self._username),
                        "password": "{}".format(self._password)
                    }
                }
            }
        ]

        req = requests.post(login_url, data=ujson.dumps(login_data))

        if 200 is req.status_code:

            self._login_time = time.time()

            resp_json = ujson.loads(req.text)

            if 0 is int(resp_json[0]["code"]):
                self._lease_time = resp_json[0]["value"]["Token"]["leaseTime"]
                self._token = resp_json[0]["value"]["Token"]["name"]
            else:
                try:
                    if "login failed" == resp_json[0]["error"]["detail"]:
                        raise exceptions.LogInException
                except KeyError:
                    raise exceptions.CameraError(resp_json)

            self._api_url = "http://{0}/cgi-bin/api.cgi?token={1}".format(self._ip_address, self._token)

        else:
            raise exceptions.CameraError(req.text)

    def request(self, request_type: str = "POST", data: str = "") -> dict:
        """
        Send basic request to Reolink API to fetch desired data
        :param request_type:
        :param data:

        :return:    The API response
        """

        # TODO Check what Exception is raised at wrong input

        if self._check_token_status:
            if "GET" is request_type:
                req = requests.get(self._api_url, data=ujson.dumps(data))
            elif "POST" is request_type:
                req = requests.post(self._api_url, data=ujson.dumps(data))
            else:
                raise ValueError("Request type unsupported")

            try:
                response = ujson.loads(req.text)[0]
            except IndexError:
                raise exceptions.CameraError

            if 0 is int(response["code"]):
                return response["value"]
            else:
                raise exceptions.CameraError

        else:
            self.login()

    def _check_token_status(self) -> bool:
        if self._token and self._lease_time and self._login_time is not None:
            current_time = time.time()
            if (current_time - self._login_time) > self._lease_time: # If lease time of token expired...
                return False                                         # ...renew it
            else:
                return True

        else:
            raise ValueError("No login data detected")
