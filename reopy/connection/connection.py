class Connection:
    """

    """

    def __init__(self, api, api_requests):
        self._api = api
        self._requests = api_requests

        self._mac_address = self._get_conn_info()["LocalLink"]["mac"]
        self._ports_services = self._get_open_ports_services()["NetPort"]

    @property
    def mac_address(self):
        """
        """

        return self._mac_address

    @property
    def ports_services(self):
        """
        """

        return self._ports_services

    def _get_open_ports_services(self):
        """
        """

        return self._api.request("POST", data=self._requests.device_open_ports_services_get)

    def _get_conn_info(self):
        """
        """

        return self._api.request("POST", data=self._requests.device_network_interface_get)
