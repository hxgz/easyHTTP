# coding:utf-8

import os
import cgi
from urllib.parse import unquote
from urllib.parse import urlparse

from .client import Client


class FileClient(Client):
    @classmethod
    def _resp_human(cls, response):
        '''处理返回数据'''

        # ct = cls.RESPONSE_CONTENT_TYPE or cgi.parse_header(
        #     response.headers.get('Content-Type', ''))[0]

        filename = os.path.split(urlparse(unquote(response.request.url)).path)[1]
        if 'Content-Disposition' in response.headers:
            try:
                cd = response.headers['Content-Disposition'].encode('ISO-8859-1').decode('utf-8')
            except:
                cd = response.headers['Content-Disposition'].encode('utf-8')

            _, dispost = cgi.parse_header(unquote(cd))

            filename = dispost.get('filename') or 'unknow_file'

        return {
            "filename": filename,
            "content": response.body,
            "size": len(response.body),
        }
