#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import os

from reopy.utility import util

class APIRequests:
    """
    All necessary API requests stored in one place, customizable
    """

    # TODO Maybe each Request should have its own JSON file?

    def __init__(self):

        self._device_general_info_get = util.FileUtil.read_json(self._get_path_to_file("device_info.json"))

        self._device_open_ports_services_get = util.FileUtil.read_json(self._get_path_to_file("ports_services.json"))

        self._device_network_interface_get = util.FileUtil.read_json(self._get_path_to_file("network_iface.json"))

    @staticmethod
    def playback_info_day(day: int, month: int, year: int) -> dict:
        """
        Return custom api request, which is then used to fetch information
        about all downloadable video files on a specified day

        :param day:
        :param month:
        :param year:

        :return:
        """

        api_request = util.FileUtil.read_json(APIRequests._get_path_to_file("playback_info_day.json"))

        api_request[0]["param"]["Search"]["StartTime"]["year"] = year
        api_request[0]["param"]["Search"]["StartTime"]["mon"] = month
        api_request[0]["param"]["Search"]["StartTime"]["day"] = day

        api_request[0]["param"]["Search"]["EndTime"]["year"] = year
        api_request[0]["param"]["Search"]["EndTime"]["mon"] = month
        api_request[0]["param"]["Search"]["EndTime"]["day"] = day

        return api_request

    @staticmethod
    def playback_info_available(year: int) -> dict:
        """
        Return custom api request, which is then used to fetch information
        about all downloadable video files on a specified day
        """

        api_request = util.FileUtil.read_json(APIRequests._get_path_to_file("playback_info.json"))

        api_request[0]["param"]["Search"]["StartTime"]["year"] = year
        api_request[0]["param"]["Search"]["EndTime"]["year"] = year

        return api_request

    @property
    def device_general_info_get(self):
        """
        Return api request, which is then used to fetch general
        information about the device itself
        """

        return self._device_general_info_get

    @property
    def device_open_ports_services_get(self):
        """
        Return api request, which is then used to fetch information
        about open ports and running services on the device
        """

        return self._device_open_ports_services_get

    @property
    def device_network_interface_get(self):
        """
        Return custom api request, which is then used to fetch information
        about interfaces used to communicate with the client by the device
        """

        return self._device_network_interface_get

    @staticmethod
    def _get_path_to_file(file_name):
        module_path = os.path.dirname(__file__)
        relative_path = "requests/{0}".format(file_name) 
        file_path = os.path.join(module_path, relative_path)

        return file_path