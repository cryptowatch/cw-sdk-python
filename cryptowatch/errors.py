class CryptowatchError(Exception):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
    ):
        super().__init__(message)

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.headers = headers or {}

    def __repr__(self):
        return "{}(message={}, http_status={})".format(
            self.__class__.__name__, self._message, self.http_status
        )


class APIResourceNotFoundError(CryptowatchError):
    pass


class APIRateLimitError(CryptowatchError):
    pass


class APIServerError(CryptowatchError):
    pass


class APIRequestError(CryptowatchError):
    pass


class APIKeyError(CryptowatchError):
    pass


class APIError(CryptowatchError):
    pass


class CredentialsFileError(CryptowatchError):
    def __repr__(self):
        return "{}(message={})".format(self.__class__.__name__, self._message)


class InvalidRequestError(CryptowatchError):
    def __repr__(self):
        return "{}(message={})".format(self.__class__.__name__, self._message)
