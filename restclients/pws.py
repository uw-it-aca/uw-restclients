"""
This is the interface for interacting with the Person Web Service.
"""

from restclients.dao import PWS_DAO
from restclients.exceptions import InvalidRegID, InvalidNetID,\
    InvalidEmployeeID, InvalidStudentNumber, InvalidIdCardPhotoSize,\
    InvalidProxRFID, DataFailureException
from restclients.models.sws import Person, Entity
from StringIO import StringIO
from urllib import urlencode
import json
import re


PERSON_PREFIX = '/identity/v1/person'
ENTITY_PREFIX = '/identity/v1/entity'
CARD_PREFIX = '/idcard/v1/card'


class PWS(object):
    """
    The PWS object has methods for getting person information.
    """
    def __init__(self, actas=None):
        self.actas = actas
        self._re_regid = re.compile(r'^[A-F0-9]{32}$', re.I)
        self._re_personal_netid = re.compile(r'^[a-z][_a-z0-9]{0,14}$', re.I)
        self._re_admin_netid = re.compile(r'^[a-z]adm_[a-z][a-z0-9]{0,14}$',
                                          re.I)
        self._re_application_netid = re.compile(r'^a_[a-z0-9\-\_\.$.]{1,18}$',
                                                re.I)
        self._re_employee_id = re.compile(r'^\d{9}$')
        self._re_student_number = re.compile(r'^\d{7}$')
        self._re_prox_rfid = re.compile(r'^\d{16}$')

    def get_person_by_regid(self, regid):
        """
        Returns a restclients.Person object for the given regid.  If the
        regid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        dao = PWS_DAO()
        url = "%s/%s/full.json" % (PERSON_PREFIX, regid.upper())
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._person_from_json(response.data)

    def get_person_by_netid(self, netid):
        """
        Returns a restclients.Person object for the given netid.  If the
        netid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwnetid(netid):
            raise InvalidNetID(netid)

        dao = PWS_DAO()
        url = "%s/%s/full.json" % (PERSON_PREFIX, netid.lower())
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._person_from_json(response.data)

    def get_person_by_employee_id(self, employee_id):
        """
        Returns a restclients.Person object for the given employee id.  If the
        employee id isn't found, or if there is an error communicating with the
        PWS, a DataFailureException will be thrown.
        """
        if not self.valid_employee_id(employee_id):
            raise InvalidEmployeeID(employee_id)

        url = "%s.json?%s" % (PERSON_PREFIX,
                              urlencode({"employee_id": employee_id}))
        response = PWS_DAO().getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        # Search does not return a full person resource
        data = json.loads(response.data)
        if not len(data["Persons"]):
            raise DataFailureException(url, 404, "No person found")

        regid = data["Persons"][0]["PersonURI"]["UWRegID"]
        return self.get_person_by_regid(regid)

    def get_person_by_student_number(self, student_number):
        """
        Returns a restclients.Person object for the given student number.  If
        the student number isn't found, or if there is an error communicating
        with the PWS, a DataFailureException will be thrown.
        """
        if not self.valid_student_number(student_number):
            raise InvalidStudentNumber(student_number)

        url = "%s.json?%s" % (PERSON_PREFIX,
                              urlencode({"student_number": student_number}))
        response = PWS_DAO().getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        # Search does not return a full person resource
        data = json.loads(response.data)
        if not len(data["Persons"]):
            raise DataFailureException(url, 404, "No person found")

        regid = data["Persons"][0]["PersonURI"]["UWRegID"]
        return self.get_person_by_regid(regid)

    def get_person_by_prox_rfid(self, prox_rfid):
        """
        Returns a restclients.Person object for the given rfid.  If the rfid
        isn't found, or if there is an error communicating with the IdCard WS,
        a DataFailureException will be thrown.
        """
        if not self.valid_prox_rfid(prox_rfid):
            raise InvalidProxRFID(prox_rfid)

        dao = PWS_DAO()
        url = "%s.json?%s" % (CARD_PREFIX,
                              urlencode({"prox_rfid": prox_rfid}))
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)
        if not len(data["Cards"]):
            raise DataFailureException(url, 404, "No card found")

        regid = data["Cards"][0]["RegID"]
        return self.get_person_by_regid(regid)

    def get_entity_by_regid(self, regid):
        """
        Returns a restclients.Entity object for the given regid.  If the
        regid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwregid(regid):
            raise InvalidRegID(regid)

        dao = PWS_DAO()
        url = "%s/%s.json" % (ENTITY_PREFIX, regid.upper())
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._entity_from_json(response.data)

    def get_entity_by_netid(self, netid):
        """
        Returns a restclients.Entity object for the given netid.  If the
        netid isn't found, or if there is an error communicating with the PWS,
        a DataFailureException will be thrown.
        """
        if not self.valid_uwnetid(netid):
            raise InvalidNetID(netid)

        dao = PWS_DAO()
        url = "%s/%s.json" % (ENTITY_PREFIX, netid.lower())
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
        url = "%s/%s/full.json" % (PERSON_PREFIX, regid.upper())
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

        return StringIO(response.data)

    def valid_uwnetid(self, netid):
        uwnetid = str(netid)
        return (self._re_personal_netid.match(uwnetid) is not None or
                self._re_admin_netid.match(uwnetid) is not None or
                self._re_application_netid.match(uwnetid) is not None)

    def valid_uwregid(self, regid):
        return True if self._re_regid.match(str(regid)) else False

    def valid_employee_id(self, employee_id):
        return True if self._re_employee_id.match(str(employee_id)) else False

    def valid_student_number(self, student_number):
        return True if (
            self._re_student_number.match(str(student_number))) else False

    def valid_prox_rfid(self, prox_rfid):
        return True if self._re_prox_rfid.match(str(prox_rfid)) else False

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

        person_affiliations = person_data.get('PersonAffiliations')
        if person_affiliations is not None:
            student_affiliations = (person_affiliations
                                    .get('StudentPersonAffiliation'))
            if student_affiliations is not None:
                person.student_number = (student_affiliations
                                         .get('StudentNumber'))
                person.student_system_key = (student_affiliations
                                             .get('StudentSystemKey'))
            employee_affiliations = (person_affiliations
                                     .get('EmployeePersonAffiliation'))
            if employee_affiliations is not None:
                person.employee_id = (employee_affiliations
                                      .get('EmployeeID'))

        for affiliation in person_data["EduPersonAffiliations"]:
            if affiliation == "student":
                person.is_student = True
            elif affiliation == "alum":
                person.is_alum = True
            elif affiliation == "staff":
                person.is_staff = True
            elif affiliation == "faculty":
                person.is_faculty = True
            elif affiliation == "employee":
                person.is_employee = True

        affiliations = person_data["PersonAffiliations"]
        if "EmployeePersonAffiliation" in affiliations:
            employee = affiliations["EmployeePersonAffiliation"]
            person.mailstop = employee["MailStop"]
            person.home_department = employee["HomeDepartment"]

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
        if "StudentPersonAffiliation" in affiliations and person.is_student:
            student = affiliations["StudentPersonAffiliation"]
            if "StudentWhitePages" in student:
                white_pages = student["StudentWhitePages"]
                if "Class" in white_pages:
                    person.student_class = white_pages["Class"]
                if "Department1" in white_pages:
                    person.student_department1 = (white_pages
                                                  .get('Department1'))
                if "Department2" in white_pages:
                    person.student_department2 = (white_pages
                                                  .get('Department2'))
                if "Department3" in white_pages:
                    person.student_department3 = (white_pages
                                                  .get('Department3'))

        return person

    def _entity_from_json(self, data):
        entity_data = json.loads(data)
        entity = Entity()
        entity.uwnetid = entity_data["UWNetID"]
        entity.uwregid = entity_data["UWRegID"]
        entity.display_name = entity_data["DisplayName"]

        return entity
