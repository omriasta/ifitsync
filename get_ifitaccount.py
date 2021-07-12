"""Get the token from iFit and return user workouts"""
import requests
import getpass
import json
import os.path
import time
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from lxml import html
import re


retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

if os.path.exists("ifit-credentials.json"):
    with open("ifit-credentials.json") as ifit_credentials_json:
        ifit_credentials = json.load(ifit_credentials_json)
    if ifit_credentials["timestamp"] + ifit_credentials["expires_in"] > time.time():
        ACCESS_TOKEN = ifit_credentials["access_token"]
        CLIENT_ID = ifit_credentials["clientid"]
        CLIENT_SECRET = ifit_credentials["clientsecret"]
    else:
        TOKEN_URL = "https://api.ifit.com/oauth/token"
        TOKEN_HEADERS = {
            "Host": "api.ifit.com",
            "Connection": "keep-alive",
            "Origin": "https://onboarding-webview.ifit.com",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Google Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Safari/537.36",
            "content-type": "application/json",
            "Accept": "*/*",
            "Referer": "https://onboarding-webview.ifit.com/0.27.0/index.html?page=login-email",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "X-Requested-With": "com.ifit.wolf",
        }

        PAYLOAD = {
            "grant_type": "refresh_token",
            "refresh_token": ifit_credentials["refresh_token"],
            "client_id": ifit_credentials["clientid"],
            "client_secret": ifit_credentials["clientsecret"],
        }
        RESPONSE = requests.post(TOKEN_URL, headers=TOKEN_HEADERS, json=PAYLOAD)
        RESPONSE_JSON = RESPONSE.json()
        RESPONSE_JSON["timestamp"] = time.time()
        RESPONSE_JSON["clientid"] = ifit_credentials["clientid"]
        RESPONSE_JSON["clientsecret"] = ifit_credentials["clientsecret"]
        with open("ifit-credentials.json", "w") as outfile:
            json.dump(RESPONSE_JSON, outfile)
        ACCESS_TOKEN = RESPONSE_JSON["access_token"]
else:
    TOKEN_URL = "https://api.ifit.com/oauth/token"
    TOKEN_HEADERS = {
        "Host": "api.ifit.com",
        "Connection": "keep-alive",
        "Origin": "https://onboarding-webview.ifit.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Google Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Safari/537.36",
        "content-type": "application/json",
        "Accept": "*/*",
        "Referer": "https://onboarding-webview.ifit.com/0.27.0/index.html?page=login-email",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Requested-With": "com.ifit.wolf",
    }
    print("iFit Username(email):")
    IFIT_USERNAME = input()
    IFIT_PASSWORD = getpass.getpass("Password:")

    clientid_url = "https://www.ifit.com/web-api/login"
    clientid_payload = {"email": IFIT_USERNAME, "password": IFIT_PASSWORD, "rememberMe": "false"}
    clientid_HEADERS = {
                "Host": "www.ifit.com",
                "Connection": "keep-alive",
                "Origin": "https://www.ifit.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Google Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Safari/537.36",
                "content-type": "application/json",
                "Accept": "*/*",
                "Referer": "https://www.ifit.com/login?next=%2Fsettings%2Fapps",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
    }


    with requests.Session() as session:
        post = session.post(clientid_url, data=clientid_payload)
        r = session.get("https://www.ifit.com/settings/apps")
        tree = html.fromstring(r.content)
        scripts = tree.xpath('.//script[contains(text(), "initialState")]')
        regex_clientid = r"'clientId':'(.*?)'"
        clientid_list = re.findall(regex_clientid, scripts[0].text_content())
        regex_clientsecret = r"'clientSecret':'(.*?)'"
        clientsecret_list = re.findall(regex_clientsecret, scripts[0].text_content())
        CLIENT_ID = clientid_list[0]
        CLIENT_SECRET = clientsecret_list[0]

    PAYLOAD = {
        "grant_type": "password",
        "username": IFIT_USERNAME,
        "password": IFIT_PASSWORD,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    RESPONSE = requests.post(TOKEN_URL, headers=TOKEN_HEADERS, json=PAYLOAD)
    RESPONSE_JSON = RESPONSE.json()
    RESPONSE_JSON["timestamp"] = time.time()
    RESPONSE_JSON["clientid"] = CLIENT_ID
    RESPONSE_JSON["clientsecret"] = CLIENT_SECRET
    with open("ifit-credentials.json", "w") as outfile:
        json.dump(RESPONSE_JSON, outfile)
    ACCESS_TOKEN = RESPONSE_JSON["access_token"]

IFIT_HIST_HEADERS = {"content-type": "application/json", "Accept": "*/*"}

IFIT_HIST_HEADERS["authorization"] = "Bearer " + ACCESS_TOKEN

IFIT_USER_INFO = http.get("https://api.ifit.com/v1/me", headers=IFIT_HIST_HEADERS)
IFIT_USER_DICT = IFIT_USER_INFO.json()
IFIT_USER_ID = IFIT_USER_DICT["id"]
'''Uncomment the first URL and comment out the second if you need to bulk upload all history'''
#IFIT_HIST_URL = "https://api.ifit.com/v1/activity_logs"
IFIT_HIST_URL = "https://api.ifit.com/v1/activity_logs/" + "?platform=android&after=&softwareNumber=424992&perPage=5"

IFIT_HIST = http.get(IFIT_HIST_URL, headers=IFIT_HIST_HEADERS)
HISTORY_JSON = IFIT_HIST.json()
