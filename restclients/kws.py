"""
This is the interface for interacting with the Key Web Service.
"""

from restclients.dao import KWS_DAO
from restclients.exceptions import DataFailureException
from restclients.models.kws import Key
from datetime import datetime
import json


ENCRYPTION_KEY_PREFIX = '/key/v1/type'


class KWS(object):
    """
    The KWS object has methods for getting key information.
    """
    def get_current_key(self, resource_name):
        """
        Returns a restclients.Key object for the given resource.  If the
        resource isn't found, or if there is an error communicating with the
        KWS, a DataFailureException will be thrown.
        """
        url = "%s/%s/encryption/current.json" % (ENCRYPTION_KEY_PREFIX,
                                                 resource_name)
        response = KWS_DAO().getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._key_from_json(response.data)

    def _key_from_json(self, data):
        """
        Internal method, for creating the Key object.
        """
        key_data = json.loads(data)
        key = Key()
        key.algorithm = key_data["Algorithm"]
        key.cipher_mode = key_data["CipherMode"]
        key.expiration = datetime.strptime(key_data["Expiration"],
                                           "%Y-%m-%dT%H:%M:%S")
        key.key_id = key_data["ID"]
        key.key = key_data["Key"]
        key.key_size = key_data["KeySize"]
        key.key_url = key_data["KeyUrl"]
        return key
