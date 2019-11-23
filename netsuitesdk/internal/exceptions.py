"""
    :class:`NetSuiteError`
    :class:`NetSuiteLoginError`
    :class:`NetSuiteRequestError`
    :class:`NetSuiteTypeError`
"""

class NetSuiteError(Exception):
    """Exception raised for errors during login or other requests (like
    get, getAll) to NetSuite."""

    def __init__(self, message, code=None):
        """
        :param str message: Text describing the error
        :param str code: Netsuite code specifying the exact error
                Possible values are listed in
        """

        self.message = message
        self.code = code

    def __str__(self):
        if self.code is None:
            return self.message
        return 'code: {}, message: {}'.format(self.code, self.message)


class NetSuiteLoginError(NetSuiteError):
    """Exception raised for errors during login to NetSuite"""

    pass

class NetSuiteRequestError(NetSuiteError):
    """Exception raised for errors during requests like get, search, .."""

    pass

class NetSuiteTypeError(NetSuiteError):
    """Exception raised when requested an invalid netsuite type"""

    pass