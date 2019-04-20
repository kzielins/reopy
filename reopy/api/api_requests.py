#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import os

from ..utility import util

class APIRequests:
    """
    All necessary API requests stored in one place, customizable
    """

    def __init__(self):

        self._general_info = self._get_req_json("device_info.json")
        self._performance = self._get_req_json("device_performance.json")
        
        self._open_ports_services_get = self._get_req_json("ports_services.json")
        self._network_interface_get = self._get_req_json("network_iface.json")

        self._image_conf_get = self._get_req_json("get_image_conf.json")
        self._image_conf_adv_get = self._get_req_json("get_image_conf_advanced.json")
        self._osd_conf_get = self._get_req_json("get_osd.json")
        self._video_audio_conf_get = self._get_req_json("get_video_audio.json")

    def playback_info_day(self, day: int, month: int, year: int) -> dict:
        """
        Return custom api request, which is then used to fetch information
        about all downloadable video files on a specified day

        :param day:
        :param month:
        :param year:

        :return:
        """

        api_request = self._get_req_json("playback_info_day.json")

        api_request[0]["param"]["Search"]["StartTime"]["year"] = year
        api_request[0]["param"]["Search"]["StartTime"]["mon"] = month
        api_request[0]["param"]["Search"]["StartTime"]["day"] = day

        api_request[0]["param"]["Search"]["EndTime"]["year"] = year
        api_request[0]["param"]["Search"]["EndTime"]["mon"] = month
        api_request[0]["param"]["Search"]["EndTime"]["day"] = day

        return api_request

    def playback_info_available(self, year: int) -> dict:
        """
        Return custom api request, which is then used to fetch information
        about all downloadable video files on a specified day
        """

        api_request = self._get_req_json("playback_info.json")

        api_request[0]["param"]["Search"]["StartTime"]["year"] = year
        api_request[0]["param"]["Search"]["EndTime"]["year"] = year

        return api_request

    @property
    def general_info(self):
        """
        Return API request, which is then used to fetch general
        information about the device itself
        """

        return self._general_info

    @property
    def performance(self):
        """
        Return API request, which is then used to fetch general
        information about the device's current performance
        """

        return self._performance

    @property
    def open_ports_services_get(self):
        """
        Return API request, which is then used to fetch information
        about open ports and running services on the device
        """

        return self._open_ports_services_get

    @property
    def network_interface_get(self):
        """
        Return API request, which is then used to fetch information
        about interfaces used to communicate with the client by the device
        """

        return self._network_interface_get

    @property
    def image_conf_get(self):
        """
        Return API request, which is then used to fetch information
        about the image configuration...
        TODO Further investigation
        """

        return self._image_conf_get

    @property
    def image_conf_adv_get(self):
        """
        Return API request, which is then used to fetch information
        about the image configuration...
        TODO Further investigation
        """

        return self._image_conf_adv_get
        
    @property
    def osd_conf_get(self):
        """
        Return API request, which is then used to fetch information
        about OSD placement (information, position, etc.)
        """

        return self._osd_conf_get

    @property
    def video_audio_conf_get(self):
        """
        Return API request, which is then used to fetch information
        about...
        TODO Further investigation
        """

        return self._video_audio_conf_get


    @staticmethod
    def _get_file_path(file_name):
        module_path = os.path.dirname(__file__)
        relative_path = "requests/{0}".format(file_name) 
        file_path = os.path.join(module_path, relative_path)

        return file_path

    def _get_req_json(self, file_name):
        return util.FileUtil.read_json(self._get_file_path(file_name))