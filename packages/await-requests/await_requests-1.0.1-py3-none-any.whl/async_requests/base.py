from .useragent import CommonAgent
from typing import Union
from . import utils
from . import exceptions

import json
import socks
import socket
import asyncio


class BaseResponse:
    '''
    This class contain some value/property of a Response from a request
    这个类包含了请求响应体总的一些属性/值
    '''

    def __init__(self) -> None:
        self._request_headers = {}
        self._response_headers = {}
        self._response_cookies = {}

        self._data = None

        self._status = ()

        self._content_type = None
        self._content_charset = 'utf-8'

        self._json_data = None

    @property
    def status(self):
        return self._status

    @property
    def content_type(self):
        return self._content_type

    @property
    def request_headers(self):
        return self._request_headers

    def set_request_headers(self, header: dict):
        self._request_headers = header

    @property
    def headers(self):
        return self._response_headers

    def set_headers(self, header: bytes):
        self._response_headers.clear()
        self._response_cookies.clear()

        header = header.decode().split('\r\n')

        status_str = header[0]
        header = header[1:]

        self._status = status_str.split(' ')[1:]
        self._status[0] = int(self._status[0])
        self._status = tuple(self._status)

        for item in header:
            if item == '':
                continue

            item_split = item.split(": ")
            k, v = item_split[0], ''.join(item_split[1:])
            if k != 'Set-Cookie':
                self._response_headers[k.capitalize()] = v
            else:
                cookies = v.split('; ')
                for c in cookies:
                    splited = c.split('=')
                    c_k, c_v = splited[0], ''.join(splited[1:])
                    self._response_cookies[c_k] = c_v

        self._update_infomation()

    def update_cookies(self, cookies: dict):
        self._response_cookies.update(cookies)

    @property
    def cookies(self):
        return self._response_cookies

    @property
    def data(self):
        return self._data

    def set_data(self, dt):
        if self._data is not None:
            raise RuntimeError('The data of response should be constant.')

        self._data = dt

    def _update_infomation(self):
        con_type = self.headers.get('Content-type', '')
        if con_type.startswith('text'):
            if 'charset=' in con_type:
                pos = con_type.find('charset=')
                self._content_charset = con_type[pos + len('charset='):]
                self._content_type = con_type[:pos]
            else:
                self._content_type = self.headers.get('Content-type', '')

        elif con_type != '':
            self._content_type = self.headers.get('Content-type', '')

    @property
    def text(self):
        if self._data is None:
            raise RuntimeError("Response doesn't contain of data.")

        return self._data.decode(self._content_charset)

    @property
    def json(self):
        if self._json_data is not None:
            return self._json_data

        self._json_data = json.loads(self.text)
        return self._json_data

    def is_json_data(self) -> bool:
        if 'json' in self._content_type:
            return True
        try:
            self._json_data = json.loads(self.text)
        except:
            return False
        else:
            return True


class BaseRequest:
    '''
    The base class of Request
    可以使用这个类创建一个HTTP/HTTPS请求
    '''

    # a static variable, all request will use this and self own header.
    # 一个公共头，设置后可以被所有的request使用，对于该request本身拥有的header
    # 会基于该公共头更新
    _common_headers = {
        'User-Agent': CommonAgent.AGENT_EDGE,
        'Upgrade-Insecure-Requests': '1',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Accept': '*/*',
        'Connection': 'close',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    _proxies_method = {
        'http': socks.HTTP,
        'https': socks.HTTP,
        'sock5': socks.SOCKS5,
    }

    _common_proxies = {}

    @classmethod
    def set_common_proxies(cls, proxies: dict):
        cls._common_proxies = proxies
        return cls

    @classmethod
    def set_common_header(cls, headers: dict):
        cls._common_headers = headers
        return cls

    @classmethod
    def update_common_header(cls, headers: dict):
        cls._common_headers.update(headers)
        return cls

    @classmethod
    def clean_common_header(cls):
        cls._common_headers = {
            'User-Agent': CommonAgent.AGENT_EDGE,
        }
        return cls

    def __init__(self, url, response_class=BaseResponse, loop=None):
        self._url_parsed = utils.split_url(url)
        # [http/https, hostname, request path]

        # url is https?
        self._use_ssl = True if self._url_parsed[0] == 'https' else False

        self._redirection_times = 5

        # the headers and cookies of request
        # 请求的 cookies 和 headers
        self._headers = {'Host': self._url_parsed[1]}
        self._cookies = {}

        # the request's proxies
        self._proxies = {}

        self._response_class = response_class

        if loop is None:
            loop = asyncio.get_running_loop()

        # get asyncio event loop
        self._loop = loop

        # for proxy
        self._socks = socks

        self._read_size = 512

    async def get_addr_info(self):
        if not self._loop.is_running():
            raise RuntimeError('No running event loop')

        try:
            result = await self._loop.getaddrinfo(
                self._url_parsed[1], self._url_parsed[0]
            )
        except socket.gaierror:
            raise exceptions.DNSException(self._url_parsed[1])

        return result

    def set_headers(self, headers: Union[dict, BaseResponse]):
        '''
        Set the headers of this request, and returns the instance itself.

        if a Response is passed to this method, this request headers will
        overcoverd by Response's request headers.

        Please don't set cookie by this method! use `class.set_cookies` or 
        `class.update_cookies`

        设置请求头，并返回请求实例本身，如果参数传递的是 Response 响应体，则会用
        响应体对应的请求头复写本请求的请求头

        请不要使用这种方法设置cookies，请使用`class.set_cookies` 或
        `class.update_cookies`
        '''
        if isinstance(headers, dict):
            self._headers = headers
        else:
            self._headers = headers.request_headers

        return self

    def update_headers(self, headers: Union[dict, BaseResponse]):
        '''
        Set the headers of this request, and returns the instance itself.

        if a Response is passed to this method, this request headers will
        updated by Response's request headers.

        Please don't set cookie by this method! use `class.set_cookies` or 
        `class.update_cookies`

        设置请求头，并返回请求实例本身，如果参数传递的是 Response 响应体，则会用
        响应体对应的请求头更新本请求的请求头

        请不要使用这种方法设置cookies，请使用`class.set_cookies` 或
        `class.update_cookies`
        '''
        if isinstance(headers, dict):
            self._headers.update(headers)
        else:
            self._headers.update(headers.request_headers)

        return self

    def clean_headers(self):
        '''
        Set the headers only contain the host.⭐
        And return the instance it self.

        将header设置为只包含host字段，并返回实例自身
        '''
        self._headers = {"Host": self._url_parsed[1]}
        return self

    @property
    def headers(self):
        res = self._common_headers.copy()
        res.update(self._headers)
        return res

    def set_cookies(self, cookies: Union[dict, BaseResponse]):
        '''
        Set the cookies of this request, and returns the instance itself.

        if a Response is passed to this method, this request cookies will
        updated by cookies from Response's 'set-cookies' header items.

        设置cookies，并返回请求实例本身，如果参数传递的是 Response 响应体，则会用
        响应体头部中'set-cookie'条目生成的cookie覆盖此请求的cookies
        '''
        if isinstance(cookies, dict):
            self._cookies = cookies
        else:
            self._headers = cookies.cookies

        return self

    def update_cookies(self, cookies: Union[dict, BaseResponse]):
        '''
        Set the cookies of this request, and returns the instance itself.

        if a Response is passed to this method, this request cookies will
        updated by cookies from Response's 'set-cookies' header items.

        设置cookies，并返回请求实例本身，如果参数传递的是 Response 响应体，则会用
        响应体头部中'set-cookie'条目生成的cookie覆盖此请求的cookies
        '''
        if isinstance(cookies, dict):
            self._cookie.update(cookies)
        else:
            self._cookie.update(cookies.cookies)

        return self

    def set_rediction_times(self, times: int):
        if times < 0:
            times = -1
        self._redirection_times = times
        return self

    @property
    def cookies(self):
        return self._cookies

    def clean_cookies(self):
        '''
        clean the cookies dict. And return the instance it self.

        清空cookies字典，并返回实例自身
        '''
        self._cookies = {}
        return self

    def set_proxies(self, proxies: dict):
        '''
        Set the proxies of this request, and returns the instance itself.

        设置代理，并返回请求实例本身
        '''
        self._proxies = proxies
        return self

    @property
    def proxies(self):
        return self._proxies

    @property
    def read_size(self):
        return self._read_size

    def set_read_size(self, size: int):
        self._read_size = size
        return self

    async def _open_connection(self, header_data: bytes, timeout: float, write_eof=True):
        '''
        A common async function for all http(s) requests. 
        It's used to open a socket to connect the target
        server.

        This method will return the request header and a
        reader and writer only. If want to get the body
        of the request, use method `_get_request_body`
        and pass in reader and writer returned by this 
        method

        对所有HTTP(s)请求通用的异步函数, 其用于打开一个socket
        并连接到目标服务器

        本方法仅仅返回请求头以及一对读写器，如果希望获得请求正文
        请使用方法`_get_request_body`，并传入本方法返回的读写器
        '''

        port = 443 if self._use_ssl else 80

        # Judge whether the current event loop is on
        # 判断当前循环是否开启

        if not self._loop.is_running():
            raise RuntimeError('no running event loop')

        proxies = __class__._common_proxies.copy()
        proxies.update(self._proxies)

        socket_ = None

        # The proxy is based on socks module.
        # 代理是基于 socks 库
        if proxies:
            try:
                if 'sock5' in proxies:
                    proxy_method = __class__._proxies_method['sock5']
                    proxy_address = utils.str2IpAndPort(proxies['sock5'])
                elif self._use_ssl:
                    proxy_method = __class__._proxies_method['https']
                    proxy_address = utils.str2IpAndPort(proxies['https'])
                else:
                    proxy_method = __class__._proxies_method['http']
                    proxy_address = utils.str2IpAndPort(proxies['http'])

                self._socks.set_default_proxy(
                    proxy_method,
                    *proxy_address
                )
            except Exception as e:
                raise ValueError('Invalid proxies value.')
            else:
                socket_ = self._socks.socksocket

        # response to be returned.
        # 用于返回的响应体
        resp = self._response_class()

        try:
            # use wait_for for enable timeout
            # 使用 wait_for 方法支持超时

            if socket_ is not None:
                # Use socks to enable proxy.
                # 使用 socks 启用代理
                sock_ = socket_(
                    socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
                sock_.connect((self._url_parsed[1], port))

                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(
                        sock=sock_,
                        ssl=self._use_ssl,
                        server_hostname=None if not self._use_ssl else self.cls[1],
                    ),
                    timeout
                )
            else:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(
                        host=self._url_parsed[1],
                        port=port,
                        ssl=self._use_ssl,
                        server_hostname=None if not self._use_ssl else self._url_parsed[1]
                    ),
                    timeout
                )

            # Write the request header to the server.
            # 将请求头写入服务器
            writer.write(header_data)
            if write_eof and writer.can_write_eof():
                writer.write_eof()

            # Enable timeout for write.
            # 启动写超时
            await asyncio.wait_for(
                writer.drain(), timeout
            )

            try:
                # read the headers of response, and enable the timeout
                # 读取请求头, 并启用超时
                response_header = await asyncio.wait_for(
                    reader.readuntil(b'\r\n\r\n'), timeout
                )
            except asyncio.exceptions.IncompleteReadError as e:
                raise e

            resp.set_headers(response_header)
            resp.update_cookies(self._cookies)

        except asyncio.exceptions.TimeoutError:
            raise exceptions.ResquestTimeoutException(self._url_parsed[1])
        except Exception as e:
            raise e

        return (reader, writer), resp
