from django.test import TestCase
from django.conf import settings
from restclients.o365.license import License
from restclients.exceptions import DataFailureException

class O365TestLicense(TestCase):

    def test_license(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            license = License()
            skus = license.get_subscribed_skus()
            self.assertEquals(len(skus), 2)
            self.assertEquals(skus[0].sku_part_number, 'PLAN_9')

    def test_set_netid_license(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            license = License()
            response = license.set_licenses_for_netid('javerage')

    def test_set_user_license(self):
        with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.o365.File'):

            license = License()
            response = license.set_user_licenses('javerage@test')
