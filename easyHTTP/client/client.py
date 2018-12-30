# coding:utf-8
import re
import cgi
import json
from urllib.parse import urlencode
import logging

from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.httpclient import HTTPError

from .mixin import SyncCallMixin


AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")


class ContentType(object):
    URLEncoded = "application/x-www-form-urlencoded"
    JSON = "application/json"
    JAVASCRIPT = "application/javascript"


class Client(SyncCallMixin):
    METHOD = "GET"
    CONTENT_TYPE = ContentType.JSON
    RESPONSE_CONTENT_TYPE = None
    TIMEOUT = 0
    FOLLOW_REDIRECTS = True

    @classmethod
    def _build_req_body(cls, data):
        if cls.METHOD == "POST" and data:
            if cls.CONTENT_TYPE == ContentType.JSON:
                return json.dumps(data)
            elif cls.CONTENT_TYPE == ContentType.URLEncoded:
                return urlencode(data)

    def _build_request(self, url, data, headers):
        final_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            # "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1"
        }
        if self.METHOD == "POST":
            final_headers["Content-Type"] = self.CONTENT_TYPE

        if headers:
            final_headers.update(headers)

        self.response_body = b''
        body = self._build_req_body(data)

        self.request = HTTPRequest(
            url, method=self.METHOD, body=body, headers=final_headers,
            request_timeout=self.TIMEOUT, follow_redirects=self.FOLLOW_REDIRECTS,
            streaming_callback=self.chunk_call,
        )

    def chunk_call(self, chunk):
        self.response_body += chunk

    async def call(self, url=None, data=None, headers=None):
        """http异步调用

        :param path_args: 命令行参数
        :param params: query参数
        :param data: body（GET 忽略）
        :param headers: Header
        """
        self._build_request(url, data, headers)

        try:
            resp = await AsyncHTTPClient().fetch(self.request)
        except HTTPError as e:
            if e.code not in [301, 302]:
                raise
            resp = e.response
        logging.debug("url:%s resp:%s ", resp.request.url, resp.body)

        self.response = resp
        self.response._body = self.response_body

        return self._parse_response(resp)

    @classmethod
    def _resp_human(cls, response):
        '''处理返回数据'''
        if response.code in (301, 302):
            return response.headers['Location']

        ct = cls.RESPONSE_CONTENT_TYPE or cgi.parse_header(response.headers['Content-Type'])[0]

        if ct.startswith('text'):  # text/html,text/plain
            return response.body.decode('utf-8')
        elif ct in ['application/json']:
            return json.loads(response.body)
        elif ct in ['application/javascript']:
            m = re.match(r'[^\(]*\((.*)\)', response.body.decode('utf-8'), re.S)

            if m:
                json_str = m.group(1).replace('\'', '"')
                return json.loads(json_str)

        logging.error('不支持content-type:%s', ct)
        raise Exception('返回数据异常, 未能正确解析')

    def transform(self, resp_data):
        '''需要继承，返回业务需要的数据'''
        return resp_data

    def _parse_response(self, resp):
        resp_data = self._resp_human(resp)
        return self.transform(resp_data)


class RedirectClient(Client):
    FOLLOW_REDIRECTS = False
