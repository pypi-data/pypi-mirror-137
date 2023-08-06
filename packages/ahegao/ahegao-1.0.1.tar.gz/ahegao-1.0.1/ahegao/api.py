import requests
import logging

from .exceptions import ApiError, AuthorizationFailed
from .__version__ import __version__, __build__

API_URL = "https://api.ahegao.ovh/"
# API_URL = "http://127.0.0.1:10808/"


class APISession:

    def __init__(self,):
        self._log = logging.getLogger("AhegaoAPI")
        self.session = requests.Session()
        # self.session.headers['Content-Type'] = "application/json"
        # self.session.headers['Accept'] = "application/json"
        self.session.headers['User-Agent'] = f"AhegaoAPI/{__version__}-{__build__}-Python"

    def __check_api(self):
        try:
            self.session.get(API_URL+"test")
        except Exception:
            raise ApiError("API not responses..")


class APIMethod:
    __slots__ = ['_api_session', '_method_name']

    def __init__(self, api_session, method_name):
        self._api_session = api_session
        self._method_name: str = method_name

    def __getattr__(self, method_name):
        return APIMethod(self._api_session, self._method_name + '.' + method_name)

    def __call__(self, **method_kwargs):
        return self._api_session(self._method_name, **method_kwargs)


class AhegaoAPI:

    def __init__(self, api_session: APISession, **kwargs):
        self.__session = api_session.session
        self.__kwargs = kwargs

    def __call__(self, method, **kwargs) -> dict:
        return self.__generate_link(method, kwargs)

    def __getattr__(self, method) -> APIMethod:
        return APIMethod(self, method)

    def __generate_link(self, method, kwargs) -> dict:
        kw = self.__kwargs.copy()
        kw.update(kwargs)

        p = kw.get("p")
        if not p:
            p = "ahegao"
        else:
            del kw['p']

        url = API_URL+p+"/"+method
        if kw.get("post"):
            r = self.__session.post(url, data=kw, params={"token": kw.get("token"), "v": kw.get("v")})
        else:
            r = self.__session.get(url, params=kw)

        return self.__error_handler(r)

    @classmethod
    def __error_handler(cls, r: requests.Response) -> ApiError or dict:
        try:
            res = r.json()
            if res['code'] != 0:
                if res['code'] == 8:
                    raise AuthorizationFailed(f"AhegaoAPI ERROR: {r.status_code}. Code: {res['code']}, Reason: {res['error']}")
                raise ApiError(f"AhegaoAPI ERROR: {r.status_code}. Code: {res['code']}, Reason: {res['error']}")
            return res
        except Exception as e:
            raise e
