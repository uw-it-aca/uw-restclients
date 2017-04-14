from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException
from vm.v1.viewmodels import Person
from unittest2 import skip


class NWSTestPerson(TestCase):
    def _assert_person_matches(self, person):
        self.assertEquals('javerage@washington.edu', person.surrogate_id)
        self.assertEquals('9136CCB8F66711D5BE060004AC494FFE', person.person_id)
        self.assertTrue(person.endpoints is not None)
        self.assertTrue(person.default_endpoint is not None)

    def test_person_by_surrogate_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            person = nws.get_person_by_surrogate_id("javerage@washington.edu")
            self._assert_person_matches(person)
            self.assertEquals(2, len(person.endpoints))

    def test_person_by_surrogate_id_nonexistent(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            self.assertRaises(DataFailureException, nws.get_person_by_surrogate_id, "asdfgh")

    @skip('Not implemented')
    def test_create_person(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            person = nws.get_person_by_surrogate_id("javerage@washington.edu")
            person.person_id = None
            person.endpoints = None

            response_status = nws.create_new_person(person)
            self.assertEquals(201, response_status)

    def test_person_by_uwregid(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            person = nws.get_person_by_uwregid("9136CCB8F66711D5BE060004AC494FFE")
            self._assert_person_matches(person)
            self.assertEquals(4, len(person.endpoints))
