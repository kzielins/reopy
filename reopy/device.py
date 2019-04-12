from reopy.api import api_requests
from reopy.api import api_handler
from reopy.playback import playback_handler
from reopy.stream import stream_handler
from reopy.connection import connection

class Device:
    """
    Representation of the actual camera, used to store basic user and device information
    """

    # TODO Make this the central class

    def __init__(self, ip_address: str, password: str, username: str = "admin"):
        self._ip_address = ip_address
        self._password = password
        self._username = username

        self._api = api_handler.BasicAPIHandler(self._password, self._username)
        self._api.login()

        self._requests = api_requests.APIRequests()
        self._connection = connection.Connection(self._api, self._requests)
        self._rec_handler = playback_handler.RecordingsHandler(self._api)

        self._model = self._get_device_model()
        self._firmware_version = self._get_firmware_version()
        self._mac_address = self._connection.mac_address

    def __repr__(self):
        return f'Camera(Model: {self._model}, Firmware_Version: {self._firmware_version}, MAC_Address: {self._mac_address}, IP: {self._ip_address})'

    def __eq__(self, other):
        if isinstance(other, Device):
            return self._mac_address == other.mac_address

        return False

    def __hash__(self):
        return hash((self._mac_address, self._ip_address, self._model))

    @property
    def mac_address(self):
        """
        MAC Address getter
        """
        return self._mac_address

    def get_general_device_info(self):
        """
        Obtain general info about the targeted device
        """

        return self._api.request("POST", data=self._requests.device_general_info_get)

    def get_available_recordings(self) -> list:
        """
        """

        return self._rec_handler.fetch_available_files()

    def download_recording(self, filename, output_name):
        """
        """

        self._rec_handler.download_file(self._ip_address, filename, output_name)

    def get_open_ports_services(self):
        return self._connection.ports_services

    def _get_firmware_version(self):
        """
        """

        return self.get_general_device_info()["DevInfo"]["firmVer"]

    def _get_device_model(self):
        """
        """

        return self.get_general_device_info()["DevInfo"]["model"]
