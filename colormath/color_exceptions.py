"""
This module contains exceptions for use throughout the L11 Colorlib.
"""
class MissingValue(Exception):
    """
    Thrown when one of the required components (Lab, LCH, etc) is missing.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)