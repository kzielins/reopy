import urllib.request
import shutil

from reopy.utility import util
from reopy.api import api_requests

class RecordingsHandler:
    """
    An interface to automatically download all stored video files on the camera
    """

    def __init__(self, api_handler):
        self._api = api_handler

    def download_file(self, filename, output_name):
        """
        Download video files from the camera
        """

        # IP modularity needed

        with urllib.request.urlopen("http://192.168.2.100/cgi-bin/api.cgi?cmd=Download&source={0}&output={0}&token={1}".format(filename, self._api.token)) as response, open(output_name, "wb") as out_file:
            shutil.copyfileobj(response, out_file)

    def fetch_available_files(self):
        """
        Fetch information about all available video files
        """

        info_video_dates = list()
        time_now = util.DateUtil.current_time(as_epoch=False)

        current_year = int(time_now["date_year"])
        current_month = int(time_now["date_month"])

        print("Fetching and processing data about available recordings...")

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

            #print(info_video_dates)

            # TODO Optimize maximum runtime (not O(n^3))

            days_total = 0
            recordings_total = 0

            for video_info in info_video_dates:
                year = video_info["year"]
                month = video_info["mon"]
                days = video_info["table"]

                days_total += len(days)

                # Obtain name of each recording on specified days

                # TODO Make it usable as a module, so no print() etc.

                for day in days:
                    available_videos_per_day = self._api.request("POST", data=api_requests.APIRequests.playback_info_day(day, month, year))

                    for elements in available_videos_per_day["SearchResult"]["File"]:
                        recordings_total += 1

            print("{0} recordings available over a duration of {1} days!".format(recordings_total, days_total))

    def _get_available_videos_per_year(self, given_month: int, given_year: int) -> list:
        available_videos = list()

        #print(given_month, given_year)

        # TODO Check type of data, so that a typecast is called only if necessary

        if 1 == int(given_month):
            for year in range(int(given_year), int(given_year-2), -1):
                available_videos.append(self._api.request("POST", data=api_requests.APIRequests.playback_info_available(year)))
        else:
            available_videos.append(self._api.request("POST", data=api_requests.APIRequests.playback_info_available(given_year)))

        return available_videos
