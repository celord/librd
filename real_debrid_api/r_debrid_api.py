import logging
from unittest import result
from real_debrid_api.auth import Auth
from real_debrid_api.rest_adapter import RestAdapter
from real_debrid_api.exceptions import RealDebridApiException
from real_debrid_api.models import *


class RealDebridApi:
    def __init__(self, hostname: str = "api.real-debrid.com/rest"):
        self._rest_adapter = RestAdapter(hostname)

    # GET api endpoints

    def get_user_info(self) -> Result:
        result = self._rest_adapter.get(endpoint="user")
        return result

    def torrents(self) -> Result:
        result = self._rest_adapter.get("torrents")
        return result

    def torrents_info(self, id: str) -> Result:
        result = self._rest_adapter.get("torrents/info/" + str(id))
        return result

    def torrents_active_count(self) -> Result:
        result = self._rest_adapter.get("torrents/activeCount")
        return result

    def torrents_availableHosts(self) -> Result:
        result = self._rest_adapter.get("torrents/availableHosts")
        return result

    def torrents_instantAvailability(self, hash: str) -> Result:
        result = self._rest_adapter.get(
            "torrents/instantAvailability/" + str(hash))
        return result

    # POST api endpoints

    def unrestrict(self, link: str) -> Result:
        data = {"link": link}
        result = self._rest_adapter.post(endpoint="unrestrict/link", data=data)
        return result

    def add_magnet(self, magnet: str) -> Result:
        data = {"magnet": magnet}
        result = self._rest_adapter.post(
            endpoint="torrents/addMagnet", data=data)
        return result

    def torrents_select_files(self, torrent_id: str, files: str) -> Result:
        data = {"files": files}
        result = self._rest_adapter.post(
            endpoint="torrents/selectFiles/" + torrent_id, data=data)
        return result
