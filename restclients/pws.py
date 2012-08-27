"""
This is the interface for interacting with the Person Web Service.
"""

from restclients.dao import PWS_DAO
from restclients.exceptions import InvalidRegID, InvalidNetID
from restclients.exceptions import DataFailureException
from restclients.models import Person
import json
import re


class PWS(object):
    """
    The PWS object has methods for getting person information.
    """

    def get_person_by_regid(self, regid):
        """
        Returns a restclients.Person object for the given regid.  If the
        regid isn't found, nothing will be returned.  If there is an error
        communicating with the PWS, a DataFailureException will be thrown.
        """
        if not re.match(r'^[A-F0-9]{32}$', regid, re.I):
            raise InvalidRegID(regid)

        dao = PWS_DAO()
        url = "/identity/v1/person/%s.json" % regid.upper()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status == 404:
            return

        if response.status != 200:
            raise DataFailureException(url, response.status, response.read())

        return self._person_from_json(response.data)

    def get_person_by_netid(self, netid):
        """
        Returns a restclients.Person object for the given netid.  If the
        netid isn't found, nothing will be returned.  If there is an error
        communicating with the PWS, a DataFailureException will be thrown.
        """

        if not re.match(r'^([a-z]adm_)?[a-z][a-z0-9]{0,7}$', netid, re.I):
            raise InvalidNetID(netid)

        dao = PWS_DAO()
        url = "/identity/v1/person.json?netid=%s" % netid.lower()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status == 404:
            return

        if response.status != 200:
            raise DataFailureException(url, response.status, response.read())

        return self._person_from_json(response.data)

    def _person_from_json(self, data):
        """
        Internal method, for creating the Person object.
        """
        person_data = json.loads(data)
        person = Person()
        person.uwnetid = person_data["UWNetID"]
        person.uwregid = person_data["UWRegID"]

        person.whitepages_publish = person_data["WhitepagesPublish"]
        person.surname = person_data["RegisteredSurname"]
        person.first_name = person_data["RegisteredFirstMiddleName"]
        person.full_name = person_data["RegisteredName"]

        return person
