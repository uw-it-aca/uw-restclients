"""
Interfacing with the Student Web Service, Person resource
"""
import logging
from restclients.models.sws import SwsPerson, StudentAddress, LastEnrolled
from restclients.sws import get_resource


logger = logging.getLogger(__name__)
sws_url_prefix = "/student/v5/person/"
sws_url_suffix = ".json"


def get_person_by_regid(regid):
    """
    Returns a restclients.models.sws.SwsPerson object
    """
    url = sws_url_prefix + regid + sws_url_suffix
    return _process_json_data(get_resource(url))


def _process_json_data(jdata):
    """
    Returns a restclients.models.sws.SwsPerson object
    """
    person = SwsPerson()
    person.directory_release = jdata["DirectoryRelease"]
    person.email = jdata["Email"]
    person.employee_id = jdata["EmployeeID"]
    person.first_name = jdata["FirstName"]
    person.gender = jdata["Gender"]
    person.last_name = jdata["LastName"]
    person.student_name = jdata["StudentName"]

    if jdata["LastEnrolled"] is not None:
        last_enrolled = LastEnrolled()
        last_enrolled.href = jdata["LastEnrolled"]["Href"]
        last_enrolled.quarter = jdata["LastEnrolled"]["Quarter"]
        last_enrolled.year = jdata["LastEnrolled"]["Year"]
        person.last_enrolled = last_enrolled
    
    if jdata["LocalAddress"] is not None:
        local_address = StudentAddress()
        local_address.city = jdata["LocalAddress"]["City"]
        local_address.country = jdata["LocalAddress"]["Country"]
        local_address.street_line1 = jdata["LocalAddress"]["Line1"]
        local_address.street_line2 = jdata["LocalAddress"]["Line2"]
        local_address.postal_code = jdata["LocalAddress"]["PostalCode"]
        local_address.state = jdata["LocalAddress"]["State"]
        local_address.zip_code = jdata["LocalAddress"]["Zip"]
        person.local_address = local_address

    person.local_phone = jdata["LocalPhone"]

    if jdata["PermanentAddress"] is not None:
        permanent_address = StudentAddress()
        permanent_address.city = jdata["PermanentAddress"]["City"]
        permanent_address.country = jdata["PermanentAddress"]["Country"]
        permanent_address.street_line1 = jdata["PermanentAddress"]["Line1"]
        permanent_address.street_line2 = jdata["PermanentAddress"]["Line2"]
        permanent_address.postal_code = jdata["PermanentAddress"]["PostalCode"]
        permanent_address.state = jdata["PermanentAddress"]["State"]
        permanent_address.zip_code = jdata["PermanentAddress"]["Zip"]
        person.permanent_address = permanent_address

    person.permanent_phone = jdata["PermanentPhone"]
    person.uwregid = jdata["RegID"]
    person.student_number = jdata["StudentNumber"]
    person.student_system_key = jdata["StudentSystemKey"]
    person.uwnetid = jdata["UWNetID"]
    person.visa_type = jdata["VisaType"]

    return person

