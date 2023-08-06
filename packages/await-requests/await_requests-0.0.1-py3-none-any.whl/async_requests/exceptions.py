'''
This module contain some request exception and function exception
'''


class UrlParseException(BaseException):
    '''
    This exception is thrown when parsing an illegal URL

    当解析一个非法的url时该异常会被throw
    '''

    def __init__(self, msg=None):
        if msg == None:
            msg = 'An illegal url is passed to parse function.'
        self._msg = msg

    def __str__(self) -> str:
        return self._msg


class DNSException(BaseException):
    def __init__(self, url):
        self._url = url

    def __str__(self) -> str:
        return "Can't parse IP address of the host '%s'" % self._url


class ResquestTimeoutException(BaseException):
    def __init__(self, url):
        self._url = url

    def __str__(self) -> str:
        return "Timeout accessing host: '%s'" % self._url
