class APIRequests:
    """
    All necessary API requests stored in one place, customizable
    """

    # TODO Maybe as DataClass?

    def __init__(self):
        self._device_general_info_get = [
            {
                "cmd": "GetDevInfo",
                "action": 0,
                "param": {}
            }
        ]

        self._device_open_ports_services_get = [
            {
                "cmd": "GetNetPort",
                "action": 0,
                "param": {}
            }
        ]

        self._device_network_interface_get = [
            {
                "cmd": "GetLocalLink",
                "action": 0,
                "param": {}
            }
        ]

    @staticmethod
    def playback_info_day(day: int, month: int, year: int) -> dict:
        """
        Returns custom api request, which is then used to fetch information
        about all downloadable video files on a specified day
        """

        api_request = [
            {
                "cmd": "Search",
                "action": 1,
                "param": {
                    "Search": {
                        "channel": 0,
                        "onlyStatus": 0,
                        "streamType": "main",
                        "StartTime": {
                            "year": 0,
                            "mon": 0,
                            "day": 0,
                            "hour": 00,
                            "min": 00,
                            "sec": 1
                        },
                        "EndTime": {
                            "year": 0,
                            "mon": 0,
                            "day": 0,
                            "hour": 23,
                            "min": 59,
                            "sec": 59
                        }
                    }
                }
            }
        ]

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
        Returns custom api request, which is then used to fetch information
        about all downloadable video files on a specified day
        """

        api_request = [
            {
                "cmd": "Search",
                "action": 1,
                "param": {
                    "Search": {
                        "channel": 0,
                        "onlyStatus": 1,
                        "streamType": "main",
                        "StartTime": {
                            "year": 2019,
                            "mon": 1,
                            "day": 1,
                            "hour": 0,
                            "min": 0,
                            "sec": 0
                        },
                        "EndTime": {
                            "year": 2019,
                            "mon": 12,
                            "day": 31,
                            "hour": 23,
                            "min": 59,
                            "sec": 59
                        }
                    }
                }
            }
        ]

        api_request[0]["param"]["Search"]["StartTime"]["year"] = year
        api_request[0]["param"]["Search"]["EndTime"]["year"] = year

        return api_request

    @property
    def device_general_info_get(self):
        """
        Returns api request, which is then used to fetch general
        information about the device itself
        """

        return self._device_general_info_get

    @property
    def device_open_ports_services_get(self):
        """
        Returns api request, which is then used to fetch information
        about open ports and running services on the device
        """

        return self._device_open_ports_services_get

    @property
    def device_network_interface_get(self):
        """
        Returns custom api request, which is then used to fetch information
        about interfaces used to communicate with the client by the device
        """

        return self._device_network_interface_get
