from typing import Optional

from falcon import testing

import eztea.json as ezjson

from ._helper import join_url_path, shorten


class CallResult:
    def __init__(self, response: testing.Result):
        self._response = response

    def __repr__(self):
        if self.is_success:
            msg = self._response.status
        else:
            msg = f"{self.error}: {shorten(self.message, 80)}"
        return f"<{type(self).__name__} {msg}>"

    @property
    def raw(self) -> testing.Result:
        return self._response

    @property
    def is_success(self):
        return 200 <= self._response.status_code <= 299

    @property
    def data(self) -> dict:
        return self._response.json

    @property
    def error(self) -> Optional[str]:
        if self.is_success:
            return None
        try:
            return self.data["error"]
        except (ezjson.JSONDecodeError, KeyError, TypeError):
            return str(self._response.status_code)

    @property
    def message(self) -> Optional[str]:
        if self.is_success:
            return None
        try:
            return self.data["message"]
        except (ezjson.JSONDecodeError, KeyError, TypeError):
            return self._response.text


class WebTestClient:
    def __init__(self, app, headers=None, prefix: str = ""):
        self.__client = testing.TestClient(app, headers=headers)
        self.__prefix = prefix

    @property
    def raw(self) -> testing.TestClient:
        return self.__client

    def get(self, path="/", **kwargs) -> testing.Result:
        """
        Simulate a GET request to a WSGI application.
        """
        return self.request("GET", path, **kwargs)

    def head(self, path="/", **kwargs) -> testing.Result:
        """
        Simulate a HEAD request to a WSGI application.
        """
        return self.request("HEAD", path, **kwargs)

    def post(self, path="/", **kwargs) -> testing.Result:
        """
        Simulate a POST request to a WSGI application.
        """
        return self.request("POST", path, **kwargs)

    def put(self, path="/", **kwargs) -> testing.Result:
        """
        Simulate a PUT request to a WSGI application.
        """
        return self.request("PUT", path, **kwargs)

    def options(self, path="/", **kwargs) -> testing.Result:
        """
        Simulate an OPTIONS request to a WSGI application.
        """
        return self.request("OPTIONS", path, **kwargs)

    def patch(self, path="/", **kwargs) -> testing.Result:
        """
        Simulate a PATCH request to a WSGI application.
        """
        return self.request("PATCH", path, **kwargs)

    def delete(self, path="/", **kwargs) -> testing.Result:
        """
        Simulate a DELETE request to a WSGI application.
        """
        return self.request("DELETE", path, **kwargs)

    def request(
        self, method="GET", path="/", *args, **kwargs
    ) -> testing.Result:
        """
        Simulate a request to a WSGI application.
        """
        path = join_url_path(self.__prefix, path)
        return self.__client.simulate_request(method, path, *args, **kwargs)

    def call(self, api: str, **kwargs) -> CallResult:
        response = self.post(f"/{api}", json=kwargs)
        return CallResult(response)
