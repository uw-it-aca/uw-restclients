from rest_base import RestBase
from django.conf import settings
import json
import re


class PWSClient(RestBase):
    URL_BASE = '/identity/v1'

    def __init__(self):
        self._cfg = {
            'host': settings.PWS_HOST,
            'port': settings.PWS_PORT,
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
        if not re.match(r'^[A-F0-9]{32}$', regid, re.I):
            raise Exception("Invalid regid: " + regid)

        return self.get_json(self.URL_BASE + '/person/%s.json' % regid.upper())

    def get_person_by_netid(self, netid):
        if not re.match(r'^([a-z]adm_)?[a-z][a-z0-9]{0,7}$', netid, re.I):
            raise Exception("Invalid netid: " + netid)

        data = self.get_persons({'uwnetid': netid.lower()})
        if len(data):
            person_data = data[0].get('PersonURI')
            if person_data:
                return self.get_person_by_regid(person_data.get('UWRegID'))

    def get_persons(self, opts={}):
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
