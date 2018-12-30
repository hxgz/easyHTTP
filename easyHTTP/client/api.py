# coding:utf-8

from urllib.parse import urlencode, urljoin

from .client import Client


class API(Client):
    HOST = None
    PATH = None
    TIMEOUT = 30

    @classmethod
    def _build_url(cls, path_args=None, params=None):
        url = urljoin(cls.HOST, cls.PATH)
        if path_args:
            url = url.format(**path_args)

        sep = "&" if "?" in url else "?"

        if params:
            url = "{}{}{}".format(url, sep, urlencode(params))
        return url

    async def call(self, path_args=None, params=None, data=None, headers=None):
        url = self._build_url(path_args, params)
        return await super(API, self).call(url, data, headers)
