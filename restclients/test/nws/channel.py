from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException


class NWSTestChannel(TestCase):
    #Expected values will have to change when the json files are updated
    def test_channel_channel_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            raw_channel_model = nws.get_channels_by_channel_id("uw_student_course_available|2012,winter,cse,120,w")
            self.assertEquals(len(raw_channel_model['Channel']), 10)
