"""Bridge: Exceptions"""


class BridgeException(BaseException):
    """Raise this when something is off."""


class BridgeConnectionClosedException(BridgeException):
    """Raise this when connection is closed."""


class BridgeAuthenticationException(BridgeException):
    """Raise this when there is an authentication issue."""
