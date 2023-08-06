from typing import Union, List, Dict
from .response import Response
from .base import BaseRequest
from .params import MultipartData
from urllib import parse
from . import utils
from . import exceptions


import json
import asyncio


class Request(BaseRequest):
    '''
    You can use this class to create a HTTP/HTTPS requests
    可以使用这个类创建一个HTTP/HTTPS请求
    '''

    def __init__(self, url, loop=None):
        # Set response class for base class
        super().__init__(url, Response, loop)

    @property
    def headers(self):
        res = super().headers.copy()
        res['Connection'] = 'Close'
        return res

    async def _get_request_body(self,
                                resp: Response,
                                reader: asyncio.streams.StreamReader,
                                writer: asyncio.streams.StreamWriter):
        '''
        Base on `_open_connection`, read the body of the request and
        set Response from `_open_connection`. Finally, this Response
        will be returned.

        在`_open_connection`的基础上，读取请求的正文，并设置到`_open_con
        nection`返回的响应体中，最后返回该响应
        '''

        recv_data = b''

        if resp.headers.get('Transfer-encoding', '') == 'chunked':
            while True:
                chunk_len_str = (await reader.readuntil(b'\r\n')).decode().rstrip()
                chunk_len = int(chunk_len_str, 16)
                if chunk_len == 0:
                    writer.close()
                    await writer.wait_closed()
                    break

                data = (await reader.readexactly(chunk_len + 2))[:-2]
                recv_data += data
        else:
            while True:
                data = await reader.read(self._read_size)
                if data:
                    recv_data += data
                else:
                    writer.close()
                    await writer.wait_closed()
                    break

        resp.set_data(recv_data)
        return resp

    async def get(self, params: dict = None, timeout=None, encode='utf-8'):
        # generate the request header string
        # 生成请求头字符串
        get_url = self._url_parsed[-1]
        if isinstance(params, dict):
            if get_url.find('?') != -1:
                get_url += '&%s' % parse.urlencode(params)
            else:
                get_url += '?%s' % parse.urlencode(params)

        request_header = utils.create_request_header(
            "GET", get_url, self.headers, self._cookies
        )
        write_data = request_header.encode()

        socket_io, resp = await self._open_connection(write_data, timeout)

        resp = await self._get_request_body(resp, *socket_io)

        if 'Location' in resp.headers and self._redirection_times != 0:
            url = resp.headers["Location"]
            if 'http' not in url:
                url = ('https:' if self._use_ssl else 'http:') + url

            resp = await Request(url) \
                .set_rediction_times(self._redirection_times - 1) \
                .get(None, timeout, encode)

        return resp

    async def head(self, timeout=None):
        request_header = utils.create_request_header(
            "HEAD", self._url_parsed[-1], self.headers, self._cookies
        )
        write_data = request_header.encode()
        (_, writer), resp = await self._open_connection(write_data, timeout)

        writer.close()
        await writer.wait_closed()

        return resp

    async def post(
        self,
        datas: Union[Dict[str, str], List[MultipartData]] = None,
        jsons: dict = None,
        timeout=None
    ):

        post_header = self.headers.copy()
        post_body = None
        if jsons:
            try:
                jsons = json.dumps(jsons, ensure_ascii=False)
            except Exception as e:
                raise e
            else:
                post_header['Content-Type'] = 'application/json;charset=UTF-8'
                post_body = jsons.encode()
        elif datas:
            post_body, type_header = utils.generate_post_body(datas)
            post_header['Content-Type'] = type_header

        post_header['Content-Length'] = len(post_body)
        request_header = utils.create_request_header(
            "POST", self._url_parsed[-1], post_header, self._cookies
        )
        write_data = request_header.encode() + post_body

        socket_io, resp = await self._open_connection(write_data, timeout, False)

        resp = await self._get_request_body(resp, *socket_io)

        return resp
