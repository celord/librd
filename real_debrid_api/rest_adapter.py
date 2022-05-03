import requests
import requests.packages
from typing import List, Dict


class RestAdapter:
    def __init__(self, hostname: str, version: str = "1.0", ssl_verify: bool = True):
        self.url = f"https://{hostname}/{version}/"
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noispection PyUnresolvedReferences
            requests.packages.urllib3.diable_warnings()

    def get(self, endpoint: str) -> List[Dict]:
        full_url = self.url + endpoint
        response = requests.get(url=full_url, verify=self._ssl_verify)
        data_out = response.json()
        if response.status_code >= 200 and response.status_code <= 299:  # OK
            return data_out
        raise Exception(data_out["error"])
