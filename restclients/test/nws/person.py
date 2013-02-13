from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException
from vm.v1.viewmodels import Person


class NWSTestPerson(TestCase):
    def _assert_person_matches(self, person):
        self.assertEquals('javerage', person.surrogate_id)
        self.assertEquals('9136CCB8F66711D5BE060004AC494FFE', person.person_id)
        endpoints = person.endpoints
        self.assertTrue(endpoints is not None)
        self.assertTrue(endpoints.view_models is not None)
        self.assertEquals(2, len(endpoints.view_models))
        self.assertTrue(person.default_endpoint is not None)

    def test_person_by_surrogate_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            person = nws.get_person_by_surrogate_id("javerage")
            self._assert_person_matches(person)

    def test_person_by_surrogate_id_nonexistent(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            self.assertRaises(DataFailureException, nws.get_person_by_surrogate_id, "asdfgh")


    def test_create_person(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            person = nws.get_person_by_surrogate_id("javerage")
            person.person_id = None
            person.endpoints = None

            response_status = nws.create_new_person(person)
            self.assertEquals(201, response_status)
