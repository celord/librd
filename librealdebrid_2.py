from real_debrid_api.auth import Auth
import requests, json

auth = Auth()
token = auth.get_credentials()["access_token"]
USER_AGENT = "librd"
headers = {"Authorization": "Bearer %s" % token, "User-Agent": USER_AGENT}


def get_user_data():
    """
    Returns some informations on the current user
    """
    data = {"url": "https://api.real-debrid.com/rest/1.0/user"}

    result = requests.get(data["url"], headers=headers)

    result = result.content.decode("utf8").replace("'", '"')
    result = json.loads(result)
    s = json.dumps(result, indent=4, sort_keys=True)  ##Pretty print
    print(result)


def get_user_download_list():
    """
    Returns some informations on the current user
    """
    data = {"url": "https://api.real-debrid.com/rest/1.0/downloads"}

    result = requests.get(data["url"], headers=headers)

    result = result.content.decode("utf8").replace("'", '"')
    result = json.loads(result)
    s = json.dumps(result, indent=4, sort_keys=True)  # Pretty print
    print(s)


def get_user_torrents_list():
    """
    Returns some informations on the current user
    """
    data = {"url": "https://api.real-debrid.com/rest/1.0/torrents"}

    result = requests.get(data["url"], headers=headers)

    result = result.content.decode("utf8").replace("'", '"')
    result = json.loads(result)
    s = json.dumps(result, indent=4, sort_keys=True)  # Pretty print
    print(s)


if __name__ == "__main__":
    get_user_torrents_list()
