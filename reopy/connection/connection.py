#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

class Connection:
    """
    A representation for the connection between the camera and the host
    """

    def __init__(self, api, api_requests):
        self._api = api
        self._requests = api_requests

    def get_connection_info(self) -> str:
        """
        Obtain information about the connection
        between the host and the device /
                the router and the device
        and other network stuff
        """

        return self._api.request("POST", data=self._requests.network_interface_get)["LocalLink"]

    def get_ports_services(self) -> dict:
        """
        Obtain information about which services run on
        which ports on the device specified
        """

        return self._api.request("POST", data=self._requests.open_ports_services_get)["NetPort"]
