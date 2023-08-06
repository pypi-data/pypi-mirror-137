'''
This module contain some functions for process HTTP problem,
for example, parse the url of http, get IP and port from a url and so on.

本模块包含一些有关于处理请求相关问题的函数，比如解析请求url，或者通过DNS从主机名
得到对应的IP和端口
'''

from .params import MultipartData
from typing import List, Union, Dict
from urllib import parse
from . import exceptions


def split_url(url: str):
    '''
    A url always consists of protocol, host and request path.
    such as [http/https]://[host name]/[request path]

    The function will return 3 part of url as protocol, 
    host and path

    url通常由协议部分，域名(主机)部分和请求路径部分构成，
    如 [http/https]://[host name]/[request path]

    该函数会返回url的这三个部分，即协议，域名以及请求路径
    '''

    prot_pos = url.find('://')
    if prot_pos == -1:
        # Can't find protocol name in the url.
        raise exceptions.UrlParseException()

    protocol_name = url[:prot_pos]
    prot_pos += 3  # + len('://')

    host_end_pos = url.find('/', prot_pos)
    if host_end_pos == -1:  # the url don't consists request path.
        host_end_pos = len(url)

    host_name = url[prot_pos: host_end_pos]

    request_path = url[host_end_pos:]
    if request_path == "":
        request_path = '/'

    return protocol_name, host_name, request_path


def create_request_header(method: str, request_path: str, headers: dict, cookies: dict):
    result_str = "{} {} HTTP/1.1\r\n{}\r\n\r\n"
    cookies_str = ";".join(["{} = {}".format(k, v)
                           for k, v in cookies.items()])
    if cookies_str != '':
        headers['cookie'] = cookies_str

    headers_str = "\r\n".join(["{}: {}".format(k, v)
                              for k, v in headers.items()])

    return result_str.format(method, request_path, headers_str)


def str2IpAndPort(IpPortStr: str):
    try:
        ip, port = IpPortStr.split(':')
    except:
        raise ValueError("param should be 'ip:port'")
    else:
        return ip, int(port)


def random_hex(len):
    from random import randint

    res = ''
    for _ in range(len):
        num = randint(0, 15)
        char = hex(num)[-1]
        if num > 9 and randint(0, 1) == 0:
            char = char.upper()

        res += char

    return res


def get_boundary():
    _POST_BOUNDARY = "--Asyncio-Requests-" + random_hex(20)
    return _POST_BOUNDARY


def generate_post_body(datas: Union[Dict[str, str], List[MultipartData]]):
    content_type = ''

    if isinstance(datas, dict):
        datas = parse.urlencode(datas)
        post_body = datas.encode()
        content_type = 'application/x-www-form-urlencoded'

    elif isinstance(datas, list):
        boundary = get_boundary()
        post_body = boundary.encode() + b'\r\n'
        body_crunk = [md.get_body() for md in datas]
        post_body += (boundary + '\r\n').encode().join(body_crunk)
        post_body += (boundary + '--').encode()
        content_type = 'multipart/form-data; boundary=%s' % boundary[2:]

    else:
        raise TypeError(
            "Parameter datas should be Dict[str, str] or List[MultipartData]."
        )

    return post_body, content_type
