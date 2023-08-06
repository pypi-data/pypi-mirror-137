'''
    A module of utility methods used for converting to and from strings

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-09-2021 09:00:27
    `memberOf`: string_conversion
    `version`: 1.0
    `method_name`: string_conversion
'''


# import json
# import hashlib
# import string
# import re
import utils.objectUtils as obj


def bool_to_string(value, **kwargs):
    '''
        Converts a boolean value to a string representation.

        ----------

        Arguments
        -------------------------
        `value` {bool}
            The boolean to convert

        Keyword Arguments
        -------------------------
        [`number`=False] {bool}
            if True, the result will be a string integer "1" for True and "0" for False.

        Return {string|None}
        ----------------------
        ("true"|"1") if the boolean is True, ("false"|"0") if it is False.

        None otherwise

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:57:03
        `memberOf`: string_conversion
        `version`: 1.0
        `method_name`: bool_to_string
    '''

    number = obj.get_kwarg(["number"], False, (bool), **kwargs)
    result = None
    if value is True:
        result = "true"
        if number is True:
            result = "1"
    if value is False:
        result = "false"
        if number is True:
            result = "0"
    return result
