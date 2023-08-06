class MultipartData:
    def __init__(self) -> None:
        self._headers = {}
        self._value = None

    def disposition(self, **kwargs):
        ''' Set Content-Disposition '''

        disposition_headers = ['form-data']
        for k, v in kwargs.items():
            disposition_headers.append('%s="%s"' % (k, v))

        self._headers["Content-Disposition"] = "; ".join(disposition_headers)
        return self

    def type(self, value):
        ''' Set Content-Type '''

        self._headers['Content-Type'] = value

        return self

    def __getattr__(self, __name: str):
        def set_value(value):
            self._headers[__name] = value
            return self

        return set_value

    def value(self, value: bytes):
        self._value = value
        return self

    def get_body(self):
        head_list = ['%s: %s' % (k, v) for k, v in self._headers.items()]
        head_bytes = '\r\n'.join(head_list).encode()

        return head_bytes + b'\r\n\r\n' + self._value + b'\r\n'
