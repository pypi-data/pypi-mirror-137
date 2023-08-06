import requests
from django.conf import settings

from incv_client.tof import TofClient


class INCVUnionClient:
    """INCV"""

    def __init__(self):
        self.__app_code = settings.APP_CODE
        self.__app_secret = settings.APP_SECRET
        self.api_domain = settings.INCV_API_DOMAIN
        self.web = self.__init_web()

    def __init_web(self):
        web = requests.session()
        web.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/83.0.4103.106 "
                "Safari/537.36 "
                "Edg/83.0.478.54"
            ),
            "INCV-APP-CODE": self.__app_code,
            "INCV-APP-SECRET": self.__app_secret,
        }
        return web

    @property
    def tof(self):
        return TofClient(self)
