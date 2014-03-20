"""
This module contains exceptions for use throughout the L11 Colorlib.
"""


class ColorMathException(Exception):
    """
    Base exception for all colormath exceptions.
    """

    pass


class UndefinedConversionError(ColorMathException):
    """
    Raised when the user asks for a color space conversion that does not exist.
    """

    def __init__(self, cobj, cs_to):
        super(UndefinedConversionError, self).__init__(cobj, cs_to)
        self.message = "Conversion from %s to %s is not defined." % (cobj, cs_to)


class InvalidIlluminantError(ColorMathException):
    """
    Raised when an invalid illuminant is set on a ColorObj.
    """

    def __init__(self, illuminant):
        super(InvalidIlluminantError, self).__init__(illuminant)
        self.message = "Invalid illuminant specified: %s" % illuminant


class InvalidObserverError(ColorMathException):
    """
    Raised when an invalid observer is set on a ColorObj.
    """

    def __init__(self, cobj):
        super(InvalidObserverError, self).__init__(cobj)
        self.message = "Invalid observer angle specified: %s" % cobj.observer
