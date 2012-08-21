"""
Contains objects used by the non-HTTP DAO implementations
"""


class MockHTTP(object):
    """
    An alternate object to HTTPResponse, for non-HTTP DAO
    implementations to use.  Implements the API of HTTPResponse
    as needed.
    """
    status = 0
    body = ""

    def read(self):
        """
        Returns the document body of the request.
        """
        return self.body
