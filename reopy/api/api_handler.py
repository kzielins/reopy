#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import sys
import time

import requests
import ujson

class BasicAPIHandler:
    """
    A very basic interface used to interact with the undocumented
    Reolink camera API
    """

    # TODO Implement LogInException
    # TODO Implement RequestTypeUnsupportedException
    # TODO Implement CameraError

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
        Log into Reolink camera interface using the api
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

        try:
            print("Attempting to log in...")
            req = requests.post(login_url, data=ujson.dumps(login_data))

            if 200 is req.status_code:
                print("Response status: 200 OK")

                self._login_time = time.time()

                resp_json = ujson.loads(req.text)

                if 0 is int(resp_json[0]["code"]):
                    print("Log-in successful...")

                    self._lease_time = resp_json[0]["value"]["Token"]["leaseTime"]
                    self._token = resp_json[0]["value"]["Token"]["name"]
                else:
                    try:
                        if resp_json[0]["error"]["detail"] == "login failed":
                            print("Entered either wrong username or wrong password...")
                            print("Log-in not successful...")
                            raise Exception
                    except KeyError:
                        print("Log-in not successful:")
                        print(resp_json)
                        raise Exception

                self._api_url = "http://{0}/cgi-bin/api.cgi?token={1}".format(self._ip_address, self._token)
                print("Obtained token {0} (lease time: {1} seconds)...".format(self._token, self._lease_time))

            else:
                print("Log-in not successful:")
                print(req.status_code, req.reason)
                print(req.text)

                raise Exception
        except Exception as e:
            print(e.args)
            sys.exit(1)

    def request(self, request_type: str = "POST", data: str = "") -> dict:
        """
        Send basic request to Reolink API to fetch desired data
        :param request_type:
        :param data:

        :return:    The API response
        """

        if self._check_token_status:
            if "GET" is request_type:
                req = requests.get(self._api_url, data=ujson.dumps(data))
            elif "POST" is request_type:
                req = requests.post(self._api_url, data=ujson.dumps(data))
            else:
                print("Request type unsupported...")
                raise Exception

            response = ujson.loads(req.text)[0]

            if 0 is int(response["code"]):
                return response["value"]
            else:
                print("Camera is unable to process request...")
                raise Exception

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
            raise Exception
