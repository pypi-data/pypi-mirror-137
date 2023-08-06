class InputFailure(Exception):
    """
    Exception raised for an input exception message.

    Args:
        exc_message:\\
        \t\\- The incorrect input reason.
    """
    __module__ = 'builtins'
    pass


class InvalidKeyError(Exception):
    """
    Exception raised for an invalid dictionary key.

    Built in KeyErrors do not format cleanly.
    """
    __module__ = 'builtins'
    pass
