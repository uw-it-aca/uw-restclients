"""
This is the interface for interacting with a SMS service.
"""
import re
from restclients.dao import SMS_DAO
from restclients.exceptions import InvalidPhoneNumber, PhoneNumberRequired


class SMSService(object):
    """
    This creates a SMS message to be sent to a destination phone number.
    """
    def create_message(self, to, body):
        if to != "":
            self.validate_phone_number(to)
        else:
            raise PhoneNumberRequired
        dao = SMS_DAO()
        return dao.create_message(to, body)

    """
    This sends a message to a destination phone number.
    """
    def send_message(self, message):
        dao = SMS_DAO()
        return dao.send_message(message)

    '''
    Validate North America phone numbers
    http://blog.stevenlevithan.com/archives/validate-phone-number
    '''
    def validate_phone_number(self, number):
        if not re.search('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$', number):
            raise InvalidPhoneNumber
