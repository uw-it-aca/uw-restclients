from rest_base import RestBase
from django.conf import settings
import json
import re


class InvalidNetID(Exception):
    """Exception for invalid netid."""
    pass


class InvalidRegID(Exception):
    """Exception for invalid regid."""
    pass


class PWSClient(RestBase):
    """
    Client for retrieving person data from the UW Person Web Service. Configuration
    parameters for this client are:

    :PWS_URL:
        The absolute URL of the PWS host. URL must include scheme and port (if not 80).
        Ex. https://ucswseval1.cac.washington.edu:443

    :PWS_CERT:
        Path of a certficate file. Required for access to eval and production PWS.
        Ex. /usr/local/ssl/foo.cert

    :PWS_KEY:
        Path of a public key file. Required for access to eval and production PWS.
        Ex. /usr/local/ssl/foo.key

    :PWS_TIMEOUT:
        Socket timeout for each individual connection, can be a float. None disables timeout.

    :PWS_LOG:
        Path of a file where logging will be written.
        Ex. /usr/local/logs/eval/log

    """
    URL_BASE = '/identity/v1'

    def __init__(self):
        self._cfg = {
            'url': settings.PWS_URL,
            'cert': settings.PWS_CERT,
            'key': settings.PWS_KEY,
            'timeout': settings.PWS_TIMEOUT,
            'log': settings.PWS_LOG,
            'logname': __name__
        }
        RestBase.__init__(self)

    def get_json(self, url, fields=None):
        headers = {'Accept': 'application/json'}
        r = self.GET(url, fields, headers)
        return json.loads(r.data)

    def get_person_by_regid(self, regid):
        """
        Returns person data for a person identified by the passed UWRegID.
        """
        if not re.match(r'^[A-F0-9]{32}$', regid, re.I):
            raise InvalidRegID(regid)

        return self.get_json(self.URL_BASE + '/person/%s.json' % regid.upper())

    def get_person_by_netid(self, netid):
        """
        Returns person data for a person identified by the passed UWNetID.
        """
        if not re.match(r'^([a-z]adm_)?[a-z][a-z0-9]{0,7}$', netid, re.I):
            raise InvalidNetID(netid)

        data = self.person_search({'uwnetid': netid.lower()})
        if len(data):
            person_data = data[0].get('PersonURI')
            if person_data:
                return self.get_person_by_regid(person_data.get('UWRegID'))

    def person_search(self, opts={}):
        """
        Search for person data. Valid parameters for searching are:

        :param uwregid:
            UW RegID

        :param uwnetid:
            UW NetID

        :param employee_id:
            Employee Identification Number (HEPPS primary identifier; 9 digits)

        :param student_number:
            UW Student number in SDB (7 digits)

        :param student_system_key:
            Unique key used in SDB to identify records (9 digits)

        :param development_id:
            UW Development Office Advance DB identification (10 digits)

        :param registered_surname:
            Official surname

        :param registered_first_middle_name:
            All but surname of official records name

        """
        fields = {
            'uwregid': '',
            'uwnetid': '',
            'employee_id': '',
            'student_number': '',
            'student_system_key': '',
            'development_id': '',
            'registered_surname': '',
            'registered_first_middle_name': '',
            'page_size': '100',
            'page_start': 1
        }
        for field in fields:
            if field in opts:
                fields[field] = opts[field]

        ret = []
        while fields['page_start']:
            data = self.get_json(self.URL_BASE + '/person.json', fields)

            persons = data.get('Persons', [])
            if not persons:
                break

            for person in persons:
                ret.append(person)

            next_page = data.get('Next', None)
            if not next_page:
                break
            else:
                fields['page_start'] = int(next_page['PageStart'])

        return ret
