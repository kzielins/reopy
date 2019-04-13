#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import urllib.request
import shutil

from reopy.utility import util
from reopy.api import api_requests

class RecordingsHandler:
    """
    An interface to automatically download all stored video files on the camera
    """

    def __init__(self, api_handler: object):
        self._api = api_handler

    def download_file(self, ip_address: str, filename: str, output_name: str = ""):
        """
        Download the provided video file in the execution folder
        Name of the recording is enough, as the API only demands the filename

        :param ip_address: The cameras IP address
        :param filename:
        :param output_name:
        """

        if "" is output_name:
            with urllib.request.urlopen("http://{0}/cgi-bin/api.cgi?cmd=Download&source={1}&output={1}&token={2}".format(ip_address, filename, self._api.token)) as response, open(filename, "wb") as out_file:
                shutil.copyfileobj(response, out_file)
        else:
            with urllib.request.urlopen("http://{0}/cgi-bin/api.cgi?cmd=Download&source={1}&output={1}&token={2}".format(ip_address, filename, self._api.token)) as response, open(output_name, "wb") as out_file:
                shutil.copyfileobj(response, out_file)

    def fetch_available_files(self, given_day: int = 0, given_month: int = 0, given_year: int = 0) -> list:
        """
        Fetch available video files
        If the arguments are not 0, only the given day will be looked up

        :param given_day:
        :param given_month:
        :param given_year:

        :return:
        """

        recordings = list()

        if given_day is not 0 and given_month is not 0 and given_year is not 0:
            recordings = self._get_available_videos_per_day(given_day, given_month, given_year)

        else:
            time_now = util.DateUtil.current_time(as_epoch=False)

            current_year = int(time_now["date_year"])
            current_month = int(time_now["date_month"])

            info_video_dates = list()

            try:
                available_videos = self._get_available_videos_per_year(current_month, current_year) # Fetch all downloadable videos from the year specified

                for available_videos_per_year in available_videos:

                    for elements in available_videos_per_year["SearchResult"]["Status"]:
                        info_video_dates.append(elements)

                    for video_info in info_video_dates:
                        available_files_days = video_info["table"]
                        days_month = list()
                        for j in range(len(available_files_days)):
                            if not available_files_days[j] == "0":
                                days_month.append(j+1)              # Fetch dates that have downloadable video files available
                        video_info["table"] = days_month

                    # TODO Optimize runtime (not O(n^3))

                    for video_info in info_video_dates:
                        year = video_info["year"]
                        month = video_info["mon"]
                        days = video_info["table"]

                        # Obtain name of each recording on specified days

                        for day in days:
                            videos_per_day = self._get_available_videos_per_day(day, month, year)

                            for video in videos_per_day:
                                recordings.append(video["name"])

                return recordings

            except KeyError:
                raise ValueError("No data available at given dates")

    def _get_available_videos_per_day(self, day: int, month: int, year: int) -> list:
        try:
            available_videos_per_day = self._api.request("POST", data=api_requests.APIRequests.playback_info_day(day, month, year))

            return [file for file in available_videos_per_day["SearchResult"]["File"]]

        except KeyError:
            raise ValueError("No data available at given day")

    def _get_available_videos_per_year(self, month: int, year: int) -> list:
        available_videos = list()

        if 1 == month:
            for each_year in range(year, year-2, -1):
                available_videos.append(self._api.request("POST", data=api_requests.APIRequests.playback_info_available(each_year)))
        else:
            available_videos.append(self._api.request("POST", data=api_requests.APIRequests.playback_info_available(year)))

        return available_videos
