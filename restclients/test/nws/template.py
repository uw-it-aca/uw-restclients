#get_template_by_surrogate_id

from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException


class NWSTestTemplate(TestCase):
    #Expected values will have to change when the json files are updated
    def test_template_surrogate_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            raw_template_model = nws.get_template_by_surrogate_id("CourseAvailableNotificationTemplate")
            self.assertEquals(len(raw_template_model), 5)
