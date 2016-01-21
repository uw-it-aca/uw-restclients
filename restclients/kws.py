"""
This is the interface for interacting with the Key Web Service.
"""

from restclients.dao import KWS_DAO
from restclients.exceptions import DataFailureException
from restclients.models.kws import Key
from datetime import datetime
import json


ENCRYPTION_KEY_PREFIX = '/key/v1'


class KWS(object):
    """
    The KWS object has methods for getting key information.
    """
    def _get_resource(self, url, headers={}):
        headers["Accept"] = "application/json"

        response = KWS_DAO().getURL(url, headers)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def get_key(self, key_id):
        """
        Returns a restclients.Key object for the given key ID.  If the
        key ID isn't found, or if there is an error communicating with the
        KWS, a DataFailureException will be thrown.
        """
        url = "%s/encryption/%s.json" % (ENCRYPTION_KEY_PREFIX, key_id)
        return self._key_from_json(self._get_resource(url))

    def get_current_key(self, resource_name):
        """
        Returns a restclients.Key object for the given resource.  If the
        resource isn't found, or if there is an error communicating with the
        KWS, a DataFailureException will be thrown.
        """
        url = "%s/type/%s/encryption/current.json" % (ENCRYPTION_KEY_PREFIX,
                                                      resource_name)
        return self._key_from_json(self._get_resource(url))

    def _key_from_json(self, data):
        """
        Internal method, for creating the Key object.
        """
        key = Key()
        key.algorithm = data["Algorithm"]
        key.cipher_mode = data["CipherMode"]
        key.expiration = datetime.strptime(data["Expiration"].split(".")[0],
                                           "%Y-%m-%dT%H:%M:%S")
        key.key_id = data["ID"]
        key.key = data["Key"]
        key.size = data["KeySize"]
        key.url = data["KeyUrl"]
        return key
