"""
Various utility functions that may be used throughout the module.
"""
from numpy import array

def color_to_numpy_array(color):
    """
    This is separated out here so one may easily convert custom objects similar
    to ColorObj.
    """
    color_array = array((
        color.spec_380nm,
        color.spec_390nm,
        color.spec_400nm,
        color.spec_410nm,
        color.spec_420nm,
        color.spec_430nm,
        color.spec_440nm,
        color.spec_450nm,
        color.spec_460nm,
        color.spec_470nm,
        color.spec_480nm,
        color.spec_490nm,
        color.spec_500nm,
        color.spec_510nm,
        color.spec_520nm,
        color.spec_530nm,
        color.spec_540nm,
        color.spec_550nm,
        color.spec_560nm,
        color.spec_570nm,
        color.spec_580nm,
        color.spec_590nm,
        color.spec_600nm,
        color.spec_610nm,
        color.spec_620nm,
        color.spec_630nm,
        color.spec_640nm,
        color.spec_650nm,
        color.spec_660nm,
        color.spec_670nm,
        color.spec_680nm,
        color.spec_690nm,
        color.spec_700nm,
        color.spec_710nm,
        color.spec_720nm,
        color.spec_730nm,
    ))
    return color_array