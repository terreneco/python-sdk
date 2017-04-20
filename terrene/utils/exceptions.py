"""
Terrene SDK's exceptions
"""


class NotFoundError(Exception):
    """
    Raised when a resource is not found
    """
    pass


class NotAuthorizedError(Exception):
    """
    Raised when an un-authorized action
    was attempted
    """
    pass


class UnknownError(Exception):
    """
    Raised when an unknown error happens
    """
    pass


class UnsupportedOperationError(Exception):
    """
    Raise when an operation is not supported
    """