from django.test import TestCase
from restclients.mailman.basic_list import _get_url_path, exists
from restclients.test import fdao_mailman_override


@fdao_mailman_override
class TestMailmanBasicList(TestCase):

    def test_get_url_path(self):
        self.assertEqual(_get_url_path('aaa_au12'),
                         ("/%s/admin/v1.0/uwnetid/available/?uwnetid=%s" %
                          ("__mock_key__", 'aaa_au12')))

    def test_exists(self):
        self.assertFalse(exists('bbio180a_au12'))
        self.assertTrue(exists('bbio180a_au13'))
        self.assertFalse(exists("tbus310a_au13"))
        self.assertTrue(exists("bill_au13"))
