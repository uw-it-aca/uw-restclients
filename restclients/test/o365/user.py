from django.test import TestCase
from django.conf import settings
from restclients.o365.user import User
from restclients.exceptions import DataFailureException

class O365TestUser(TestCase):

    def test_user_info(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            user = User()
            u = user.get_user('javerage')
            self.assertEquals(len(u.assigned_plans), 7)
            self.assertEquals(u.user_principal_name, 'javerage@dogfood.com')

    def test_netid_info(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            user = User()
            u = user.get_user_by_netid('javerage')
            self.assertEquals(u.dir_sync_enabled, True)
            self.assertEquals(len(u.assigned_plans), 0)
            self.assertEquals(len(u.assigned_licenses), 0)
            self.assertEquals(u.mail_nick_name, 'javerage')

    def test_user_property(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            user = User()
            u = user.get_user_property('javerage', 'usageLocation')

    def test_netid_property(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            user = User()
            u = user.get_property_for_netid('javerage', 'usageLocation')

    def test_user_location(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            user = User()
            u = user.get_user_location('javerage')

    def test_netid_location(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            user = User()
            u = user.get_location_for_netid('javerage')

    def test_set_user_property(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            user = User()
            u = user.set_user_property('javerage', 'usageLocation', 'US')

    def test_netid_property(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            user = User()
            u = user.set_property_for_netid('javerage', 'usageLocation', 'US')

    def test_set_user_location(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            user = User()
            u = user.set_user_location('javerage', 'US')

    def test_set_netid_location(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            user = User()
            u = user.set_location_for_netid('javerage', 'US')
