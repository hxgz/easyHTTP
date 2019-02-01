#! coding:utf-8
from http.cookies import SimpleCookie

from .mixin import SyncCallMixin


class Session(SyncCallMixin):
    def __init__(self, cookies=None):
        self.cookie = SimpleCookie(cookies)

    def _get_cookie(self, response):
        for c in response.headers.get_list("Set-Cookie"):
            self.cookie.load(c)

    def cookie_output(self, keys=None):
        if keys:
            _ck = SimpleCookie({
                k: v
                for k, v in self.cookie.items()
                if k in keys
            })
            return _ck.output(attrs=[], header="", sep=";")
        else:
            return self.cookie.output(attrs=[], header="", sep=";")

    async def call(self, client, *args, **kwargs):
        headers = kwargs.get('headers', {})

        if self.cookie:
            headers['Cookie'] = self.cookie_output()
            kwargs['headers'] = headers
        cli = client()
        data = await cli.call(*args, **kwargs)
        self._get_cookie(cli.response)
        return data
