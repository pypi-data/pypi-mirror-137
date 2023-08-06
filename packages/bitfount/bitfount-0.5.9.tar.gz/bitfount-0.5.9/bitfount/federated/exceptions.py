"""Custom exceptions for the federated package."""
from bitfount.exceptions import BitfountError


class BitfountTaskStartError(BitfountError, RuntimeError):
    """Raised when an issue occurs whilst trying to start a task with pods."""

    pass


class MessageHandlerNotFoundError(BitfountError, KeyError):
    """Error raised when registered message handler can't be found."""

    pass


class MessageRetrievalError(BitfountError, RuntimeError):
    """Raised when an error occurs whilst retrieving a message from message service."""

    pass


class PodConnectFailedError(BitfountError, TypeError):
    """The message service has not correctly connected the pod."""

    pass


class PodRegistrationError(BitfountError):
    """Error related to registering a Pod with BitfountHub."""

    pass


class SecureShareError(BitfountError):
    """Error related to SecureShare processes."""

    pass
