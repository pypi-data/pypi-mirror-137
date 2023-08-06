"""Exceptions for the MiCADO Parser"""


class ValidationError(Exception):
    """Base error for validation"""

    def __init__(self, error, header="Error while parsing..."):
        self.msg = header
        self.msg += f"\n  {error}"

    def __str__(self):
        """Overload __str__ to return msg when printing/logging"""
        return self.msg + "\n"


class MultiError(ValidationError):
    """Errors occured during validation..."""

    def __init__(self, error_set, header="Multiple issues in parsed ADT..."):
        self.msg = header
        for error in error_set:
            self.msg += "\n  {}".format(error)
