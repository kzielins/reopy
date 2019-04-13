#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from reopy.api import api_requests, api_handler
from reopy.playback import playback_handler
from reopy.stream import stream_handler
from reopy.connection import connection

class Device:
    """
    Representation of the actual camera, used to store basic user and device information
    """

    def __init__(self, ip_address: str, password: str, username: str = "admin"):
        self._ip_address = ip_address
        self._password = password
        self._username = username

        self._api = api_handler.BasicAPIHandler(self._ip_address, self._password, self._username)
        self._api.login()

        self._requests = api_requests.APIRequests()
        self._connection = connection.Connection(self._api, self._requests)
        self._rec_handler = playback_handler.RecordingsHandler(self._api)

        self._model = self._get_device_model()
        self._firmware_version = self._get_firmware_version()
        self._mac_address = self._connection.mac_address

    def __repr__(self) -> str:
        return f'Camera(Model: {self._model}, Firmware_Version: {self._firmware_version}, MAC_Address: {self._mac_address}, IP: {self._ip_address})'

    def __eq__(self, other) -> bool:
        if isinstance(other, Device):
            return self._mac_address == other.mac_address

        return False

    def __hash__(self):
        return hash((self._mac_address, self._ip_address, self._model))

    @property
    def mac_address(self) -> str:
        """
        MAC address getter
        """

        return self._mac_address

    def get_device_info(self) -> dict:
        """
        Obtain general info about the targeted device
        """

        return self._api.request("POST", data=self._requests.device_general_info_get)

    def get_available_recordings(self, day: int = 0, month: int = 0, year: int = 0) -> list:
        """
        Fetch available video files
        If the arguments are not 0, only the given day will be looked up

        :param day:
        :param month:
        :param year:

        :return:
        """

        return self._rec_handler.fetch_available_files(day, month, year)

    def download_recording(self, filename: str, output_name: str = ""):
        """
        Download the provided video file in the execution folder
        Name of the recording is enough, as the API only demands the filename

        :param filename:
        :param output_name:
        """

        self._rec_handler.download_file(self._ip_address, filename, output_name)

    def get_open_ports_services(self) -> dict:
        """
        Get a map of open ports and services on the device
        """

        return self._connection.ports_services

    def _get_firmware_version(self):
        return self.get_device_info()["DevInfo"]["firmVer"]

    def _get_device_model(self):
        return self.get_device_info()["DevInfo"]["model"]
