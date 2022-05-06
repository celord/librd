import logging
import requests
import requests.packages
from json import JSONDecodeError
from typing import List, Dict
from real_debrid_api.auth import Auth
from real_debrid_api.exceptions import RealDebridApiException
from real_debrid_api.models import Result


class RestAdapter:
    def __init__(
            self, hostname: str, version: str = "1.0", ssl_verify: bool = True, access_token: str = "", logger: logging.Logger = None):
        """
        Constructor for RestAdapter
        :param hostname: Normally,api.real-debrid.com/rest
        :param api_key: string used for authentication when POSTing or DELETEing
        :param ver: always 1.0
        :param ssl_verify: Normally set to True, but if having SSL/TLS cert validation issues, can turn off with False
        :param logger: (optional) If your app has a logger, pass it in here.
        """
        self.url = f"https://{hostname}/{version}/"
        self._ssl_verify = ssl_verify
        self._access_token = Auth().get_credentials()
        self._access_token = self._access_token["access_token"]
        self._logger = logger or logging.getLogger(__name__)
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X)"
        self.headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-type": "multipart/form-data;",
            "User-Agent": self.user_agent,
        }
        if not ssl_verify:
            # noispection PyUnresolvedReferences
            requests.packages.urllib3.diable_warnings()
        logging.basicConfig(level=logging.DEBUG)

    def _do(self, http_method: str, endpoint: str, ep_params: Dict = None,
            data: Dict = None, files: Dict = None) -> Result:
        full_url = self.url + endpoint
        log_line_pre = f"method={http_method}, url={full_url}"
        log_line_post = log_line_pre + " success={},status_code={},message={},"

        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(http_method, url=full_url, verify=self._ssl_verify,
                                        headers=self.headers, params=ep_params, data=data, files=files)

        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise RealDebridApiException("Request Failed") from e
        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise RealDebridApiException("Bad JSON in response") from e

        # If status_code in 200-299 range, return success Result with data, otherwise raise exception

        is_success = 299 >= response.status_code >= 200  # 200-299 range is OK
        log_line = log_line_post.format(
            is_success, response.status_code, response.reason
        )
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code, message=response.reason, data=data_out)
        self._logger.error(msg=log_line)
        raise RealDebridApiException(
            f"{response.status_code}:{response.reason}")

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        return self._do(http_method="GET", endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, data: Dict = None) -> Result:
        self._logger.debug(msg=data)
        return self._do(http_method="POST", endpoint=endpoint, data=data)
