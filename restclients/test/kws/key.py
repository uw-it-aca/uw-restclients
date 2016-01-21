from django.test import TestCase
from django.conf import settings
from restclients.kws import KWS
from restclients.exceptions import DataFailureException


class KWSTestKeyData(TestCase):

    def test_current_key(self):
        with self.settings(
                RESTCLIENTS_KWS_DAO_CLASS='restclients.dao_implementation.kws.File'):

            kws = KWS()
            key = kws.get_current_key('uw-student-registration')
            self.assertEquals(key.algorithm, 'AES128CBC', 'Correct algorithm')
            self.assertEquals(key.cipher_mode, 'CBC', 'Correct cipher mode')
            self.assertEquals(key.expiration.isoformat(), '2013-04-11T13:44:33', 'Correct expiration')
            self.assertEquals(key.key_id, 'ee99defd-baee-43b0-9e1e-f8238dd106bb', 'Correct key ID')
            self.assertEquals(key.key, 'Uv2JsxggfxF9OQNzIxAzDQ==', 'Correct key')
            self.assertEquals(key.size, 128, 'Correct key size')
            self.assertEquals(key.url, 'https://it-wseval1.s.uw.edu/key/v1/encryption/ee99defd-baee-43b0-9e1e-f8238dd106bb.json', 'Correct key URL')
