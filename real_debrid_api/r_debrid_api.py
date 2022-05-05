import logging
from real_debrid_api.rest_adapter import RestAdapter
from real_debrid_api.exceptions import RealDebridApiException
from real_debrid_api.models import *


class RealDebridApi:
    def __init__(self, hostname: str = "api.real-debrid.com/rest"):
        self._rest_adapter = RestAdapter(hostname)

    def get_user_info(self) -> Result:
        result = self._rest_adapter.get(endpoint="user")
        return result
