"""
This module contains exceptions for use throughout the L11 Colorlib.
"""
class BaseException(Exception):
    def __str__(self):
        return repr(self.value)

class MissingValue(BaseException):
    """
    Raised when one of the required components (Lab, LCH, etc) is missing.
    """
    def __init__(self, cobj, missing_val_name):
        self.value = "Missing %s value on %s." % (missing_val_name, 
                                                  cobj.__class__.__name__)
        
class InvalidValue(BaseException):
    """
    Raised when one of the required components is invalid.
    """
    def __init__(self, cobj, invalid_val_name, invalid_val):
        self.value = "Invalid %s value (%s) on %s." % (invalid_val_name,
                                                       invalid_val, 
                                                       cobj.__class__.__name__)
        
class InvalidDeltaEMode(BaseException):
    """
    Raised when an invalid Delta E mode is specified.
    """
    def __init__(self, mode):
        self.value = "Invalid Delta E mode: %s" % mode
        
class InvalidArgument(BaseException):
    """
    Raised when an invalid argument is passed to a function.
    """
    def __init__(self, function_name, invalid_arg_name, invalid_arg):
        self.value = "Invalid argument for %s (%s) passed to %s()." % (
                                                            invalid_arg_name,
                                                            invalid_arg,
                                                            function_name)
    
class InvalidConversion(BaseException):
    """
    Raised when the user asks for a color space conversion that does not exist.
    """
    def __init__(self, cobj, cs_to):
        self.value = "Conversion from %s to %s is not defined." % (cobj, cs_to)
    
class InvalidIlluminant(BaseException):
    """
    Raised when an invalid illuminant is set on a ColorObj.
    """
    def __init__(self, cobj):
        self.value = "Invalid illuminant specified: %s" % (cobj.illuminant)
    
class InvalidObserver(BaseException):
    """
    Raised when an invalid observer is set on a ColorObj.
    """
    def __init__(self, cobj):
        self.value = "Invalid observer angle specified: %s" % (cobj.observer)