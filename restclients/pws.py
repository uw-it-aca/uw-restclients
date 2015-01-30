"""
This is the interface for interacting with the Person Web Service.
"""

from restclients.dao import PWS_DAO
from restclients.exceptions import InvalidRegID, InvalidNetID, InvalidEmployeeID
from restclients.exceptions import InvalidIdCardPhotoSize
from restclients.exceptions import DataFailureException
from restclients.models.sws import Person, Entity

try:
    from urllib.parse import urlencode
except Exception:
    from urllib import urlencode
import json
import re


class PWS(object):
    """
    The PWS object has methods for getting person information.
    """
    def __init__(self, actas=None):
        self.actas = actas
        self._re_regid = re.compile(r'^[A-F0-9]{32}$', re.I)
        self._re_personal_netid = re.compile(r'^[a-z][a-z0-9]{0,7}$', re.I)
        self._re_admin_netid = re.compile(r'^[a-z]adm_[a-z][a-z0-9]{0,7}$', re.I)
        self._re_application_netid = re.compile(r'^a_[a-z0-9\-\_\.$.]{1,18}$', re.I)
        self._re_employee_id = re.compile(r'^\d{9}$')

    def get_person_by_regid(self, regid):
        """
        Returns a restclients.Person object for the given regid.  If the
        regid isn't found, nothing will be returned.  If there is an error
        communicating with the PWS, a DataFailureException will be thrown.
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        dao = PWS_DAO()
        url = "/identity/v1/person/%s/full.json" % regid.upper()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._person_from_json(response.data)

    def get_person_by_netid(self, netid):
        """
        Returns a restclients.Person object for the given netid.  If the
        netid isn't found, nothing will be returned.  If there is an error
        communicating with the PWS, a DataFailureException will be thrown.
        """
        if not self.valid_uwnetid(netid):
            raise InvalidNetID(netid)

        dao = PWS_DAO()
        url = "/identity/v1/person/%s/full.json" % netid.lower()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._person_from_json(response.data)

    def get_person_by_employee_id(self, employee_id):
        """
        Returns a restclients.Person object for the given employee id.  If the
        employee id isn't found, nothing will be returned. If there is an error
        communicating with the PWS, a DataFailureException will be thrown.
        """
        if not self.valid_employee_id(employee_id):
            raise InvalidEmployeeID(employee_id)

        url = "/identity/v1/person.json?%s" % urlencode({"employee_id": employee_id})
        response = PWS_DAO().getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        # Search does not return a full person resource
        data = json.loads(response.data)
        if len(data["Persons"]):
            regid = data["Persons"][0]["PersonURI"]["UWRegID"]
            return self.get_person_by_regid(regid)

    def get_entity_by_regid(self, regid):
        """
        Returns a restclients.Entity object for the given regid.  If the
        regid isn't found, nothing will be returned.  If there is an error
        communicating with the PWS, a DataFailureException will be thrown.
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        dao = PWS_DAO()
        url = "/identity/v1/entity/%s.json" % regid.upper()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._entity_from_json(response.data)

    def get_entity_by_netid(self, netid):
        """
        Returns a restclients.Entity object for the given netid.  If the
        netid isn't found, nothing will be returned.  If there is an error
        communicating with the PWS, a DataFailureException will be thrown.
        """
        if not self.valid_uwnetid(netid):
            raise InvalidNetID(netid)

        dao = PWS_DAO()
        url = "/identity/v1/entity/%s.json" % netid.lower()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._entity_from_json(response.data)

    def get_contact(self, regid):
        """
        Returns data for the given regid.
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        dao = PWS_DAO()
        url = "/identity/v1/person/%s/full.json" % regid.upper()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status == 404:
            return

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def get_idcard_photo(self, regid, size="medium"):
        """
        Returns a jpeg image, for the passed uwregid. Size is configured as:
            "small" (20w x 25h px),
            "medium" (120w x 150h px),
            "large" (240w x 300h px),
            {height in pixels} (custom height, default aspect ratio)
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        size = str(size)
        if (not re.match(r"(?:small|medium|large)$", size) and
                not re.match(r"[1-9]\d{1,3}$", size)):
            raise InvalidIdCardPhotoSize(size)

        url = "/idcard/v1/photo/%s-%s.jpg" % (regid.upper(), size)

        headers = {"Accept": "image/jpeg"}

        if self.actas is not None:
            if not self.valid_uwnetid(self.actas):
                raise InvalidNetID(self.actas)
            headers["X-UW-Act-as"] = self.actas

        response = PWS_DAO().getURL(url, headers)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return response.data

    def valid_uwnetid(self, netid):
        uwnetid = str(netid)
        return (self._re_personal_netid.match(uwnetid) != None
                or self._re_admin_netid.match(uwnetid) != None
                or self._re_application_netid.match(uwnetid) != None)

    def valid_uwregid(self, regid):
        return True if self._re_regid.match(str(regid)) else False

    def valid_employee_id(self, employee_id):
        return True if self._re_employee_id.match(str(employee_id)) else False

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
        person.display_name = person_data["DisplayName"]

        for affiliation in person_data["EduPersonAffiliations"]:
            if affiliation == "student":
                person.is_student = True
            if affiliation == "staff":
                person.is_staff = True
            if affiliation == "faculty":
                person.is_faculty = True
            if affiliation == "employee":
                person.is_employee = True

                # This is for MUWM-417
                affiliations = person_data["PersonAffiliations"]
                if "EmployeePersonAffiliation" in affiliations:
                    employee = affiliations["EmployeePersonAffiliation"]
                    white_pages = employee["EmployeeWhitePages"]

                    if not white_pages["PublishInDirectory"]:
                        person.whitepages_publish = False
                    else:
                        person.email1 = white_pages["Email1"]
                        person.email2 = white_pages["Email2"]
                        person.phone1 = white_pages["Phone1"]
                        person.phone2 = white_pages["Phone2"]
                        person.title1 = white_pages["Title1"]
                        person.title2 = white_pages["Title2"]
                        person.voicemail = white_pages["VoiceMail"]
                        person.fax = white_pages["Fax"]
                        person.touchdial = white_pages["TouchDial"]
                        person.address1 = white_pages["Address1"]
                        person.address2 = white_pages["Address2"]
                        person.mailstop = employee["MailStop"]
                if affiliation == "alum":
                    person.is_alum = True

        return person

    def _entity_from_json(self, data):
        entity_data = json.loads(data)
        entity = Entity()
        entity.uwnetid = entity_data["UWNetID"]
        entity.uwregid = entity_data["UWRegID"]
        entity.display_name = entity_data["DisplayName"]

        return entity
