#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import time

import ujson

class DateUtil:
    """
    A simple way to retrieve the current date in different formats
    """

    @staticmethod
    def current_time(as_epoch: bool = True):
        """
        Return current time

        :param as_epoch:    Whether or not the time current time
        should be returned as a UNIX epoch
        (Default: True)
        Otherwise: current time will be returned as verbose dict

        :return:
        """

        time_now_struct = time.time()

        if as_epoch:
            time_now = time_now_struct
        else:
            time_struct = time.localtime(time_now_struct)
            time_now = {
                "day_name": DateUtil._convert_time("%A", time_struct),
                "month_name": DateUtil._convert_time("%B", time_struct),
                "date_day": DateUtil._convert_time("%d", time_struct),
                "date_month": DateUtil._convert_time("%m", time_struct),
                "date_year": DateUtil._convert_time("%Y", time_struct),
                "time_hour": DateUtil._convert_time("%H", time_struct),
                "time_minute": DateUtil._convert_time("%M", time_struct),
                "time_second": DateUtil._convert_time("%S", time_struct)
            }


        return time_now

    @staticmethod
    def _convert_time(format_string: str, time_struct) -> str:
        return time.strftime(format_string, time_struct)

class FileUtil:
    """
    A simple wrapper around file I/O
    """

    @staticmethod
    def read_json(file_path) -> dict:
        """
        Read JSON data from desired file
        """

        with open(file_path, "r") as json_file:
            return ujson.load(json_file)
