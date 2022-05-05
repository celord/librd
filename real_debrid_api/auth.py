import requests
import json
import urllib3
from time import sleep


class Auth:
    def __init__(self):

        self.CLIENT_ID = "X245A4XAIBGVM"
        self.USER_AGENT = "librd"
        self.headers = {"User-Agent": self.USER_AGENT}
        self.url = (
            "https://api.real-debrid.com/oauth/v2/device/code?client_id=%s&new_credentials=yes"
            % (self.CLIENT_ID)
        )
        self.grant_type = "http://oauth.net/grant_type/device/1.0"

    def authenticate(self):
        """
        Authenticas the user with real-debrid.com
        """

        self.result = requests.get(self.url)
        self.result = self.result.json()
        self.device_code = self.result["device_code"]
        self.user_code = self.result["user_code"]
        print(
            "Please visit: {} and paste this code {} to authenticate, this code will expire in 5 minutes. ".format(
                self.result["verification_url"], self.result["user_code"]
            )
        )

        self.data = {}
        for i in range(0, 3600):
            try:
                sleep(1)
                url = (
                    "https://api.real-debrid.com/oauth/v2/device/credentials?client_id=%s&code=%s"
                    % (self.CLIENT_ID, self.device_code)
                )

                self.result = requests.get(url)
                self.result = self.result.json()
                if "client_secret" in self.result:
                    self.client_secret = self.result["client_secret"]
                    self.client_id = self.result["client_id"]

                    break
            except:
                pass

        self.url = "https://api.real-debrid.com/oauth/v2/token"
        self.data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.device_code,
            "grant_type": self.grant_type,
        }

        self.result = requests.post(self.url, data=self.data)
        self.result = self.result.json()
        self.data["access_token"] = self.result["access_token"]
        self.data["expires_in"] = self.result["expires_in"]
        self.data["refresh_token"] = self.result["refresh_token"]
        self.data["token_type"] = self.result["token_type"]

        with open("auth.json", "w") as auth:
            json.dump(self.data, auth)

    def refresh_authentication(self):
        """
        Refresh the authentication with real-debrid
        """

        with open("auth.json", "r") as auth:
            self.jsonfile = json.load(auth)
        self.url = "https://api.real-debrid.com/oauth/v2/token"

        self.data = {
            "client_id": self.jsonfile["client_id"],
            "client_secret": self.jsonfile["client_secret"],
            "code": self.jsonfile["refresh_token"],
            "grant_type": self.jsonfile["grant_type"],
        }
        self.result = requests.post(self.url, self.data)
        if self.result.status_code == 200:
            self.result = self.result.json()

        self.data["access_token"] = self.result["access_token"]
        self.data["expires_in"] = self.result["expires_in"]
        self.data["refresh_token"] = self.result["refresh_token"]
        self.data["token_type"] = self.result["token_type"]

        with open("auth.json", "w") as auth:
            json.dump(self.data, auth)

    def get_credentials(self): 
        """
        Returns the current credentials
        """
        try:
            with open("auth.json", "r") as auth:
                self.credentials = json.load(auth)
            return self.credentials
        except Exception as e:
            print(f"Get credentials failed: {e}")
            self.authenticate()
            self.get_credentials()
