"""
This module contains exceptions for use throughout the L11 Colorlib.
"""
class MissingValue(Exception):
    """
    Raised when one of the required components (Lab, LCH, etc) is missing.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class InvalidConversion(Exception):
    """
    Raised when the user asks for a color space conversion that does not exist.
    """
    def __init__(self, cobj, cs_to):
        self.value = "Conversion from %s to %s is not defined." % (cobj, cs_to)
    def __str__(self):
        return repr(self.value)
    
class InvalidIlluminant(Exception):
    """
    Raised when an invalid illuminant is set on a ColorObj.
    """
    def __init__(self, cobj):
        self.value = "Invalid illuminant specified: %s" % (cobj.illuminant)
    def __str__(self):
        return repr(self.value)
    
class InvalidObserver(Exception):
    """
    Raised when an invalid observer is set on a ColorObj.
    """
    def __init__(self, cobj):
        self.value = "Invalid observer angle specified: %s" % (cobj.observer)
    def __str__(self):
        return repr(self.value)