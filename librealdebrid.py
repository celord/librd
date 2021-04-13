import requests,urllib3
from time import sleep

CLIENT_ID = 'X245A4XAIBGVM'
USER_AGENT = 'librd'
headers = {'User-Agent': USER_AGENT}
url = 'https://api.real-debrid.com/oauth/v2/device/code?client_id=%s&new_credentials=yes' % (
    CLIENT_ID)

#Request the user code to enter in https://real-debrid.com/device
result = requests.get(url)
result = result.json()
device_code = result['device_code']
user_code = result['user_code']
print("Device Code: {} ".format(device_code))
print("User Code: {} ".format(user_code))


for i in range(3600):
    try:
        sleep(5)
        url = 'https://api.real-debrid.com/oauth/v2/device/credentials?client_id=%s&code=%s' % (
            CLIENT_ID, device_code)
        print("FOR Device Code: {} ".format(device_code))
        print("FOR User Code: {} ".format(user_code))
        result = requests.get(url)
        result = result.json()
        print(result)
        if 'client_secret' in result: break
    except:
        pass

