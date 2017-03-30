"""
Contains the custom exceptions used by the restclients.
"""
from restclients_core.exceptions import (InvalidRegID, InvalidNetID,
                                         InvalidEmployeeID,
                                         DataFailureException)
from uw_pws.exceptions import (InvalidStudentNumber, InvalidIdCardPhotoSize,
                               InvalidProxRFID)
from uw_sws.exceptions import (InvalidCanvasSection,
                               InvalidCanvasIndependentStudyCourse,
                               InvalidSectionID, InvalidSectionURL)

from uw_nws.exceptions import InvalidUUID


class PhoneNumberRequired(Exception):
    """Exception for missing phone number."""
    pass


class InvalidPhoneNumber(Exception):
    """Exception for invalid phone numbers."""
    pass


class InvalidGroupID(Exception):
    """Exception for invalid group id."""
    pass


class InvalidEndpointProtocol(Exception):
    """Exception for invalid endpoint protocol."""
    pass


class InvalidGradebookID:
    """Exception for invalid gradebook id."""
    pass
