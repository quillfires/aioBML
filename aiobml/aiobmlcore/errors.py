
__all__ = (
    'BMLIOException',
    'AuthenticationError',
    'ClientError',
    'InvalidContent',
    'HTTPException',
    'Unauthorized',
)


class BMLIOException(Exception):
    """Base exception class."""


class AuthenticationError(BMLIOException):
    """Authentication error."""


class ClientError(BMLIOException):
    pass


class InvalidContent(BMLIOException):
    pass


class HTTPException(BMLIOException):
    pass


class Unauthorized(HTTPException):
    pass
