"""
Provides Office 365 license services via graph web services.
"""
from django.conf import settings
from restclients.o365 import O365
from restclients.o365.user import User
from restclients.models.o365 import SKU


class License(O365):
    def get_subscribed_skus(self):
        url = '/subscribedSkus'
        data = self.get_resource(url)
        skus = []
        for sku in data.get('value', []):
            skus.append(SKU().from_json(sku))

        return skus

    def get_user_licenses(self, user):
        user = User().get_user(user)
        return user.assigned_licenses

    def get_licenses_for_netid(self, netid):
        user = User().get_user_by_netid(netid)
        return user.assigned_licenses

    def set_user_licenses(self, user, add=None, remove=None):
        """Implements: https://msdn.microsoft.com/library/azure/ad/graph/api/functions-and-actions#assignLicense
        """
        url = '/users/%s' % (user)
        body = {
            'addLicenses': add if add else null,
            'removeLicenses': remove if remove else null
        }
        data = self._put_resource(url, headers, json=body)
        return data

    def set_licenses_for_netid(self, netid, add=None, remove=None):
        user = '%s@%s' % (
            netid, settings.RESTCLIENTS_O365_PRINCIPLE_DOMAIAN)
        return self.set_user_licenses(user, add=add, remove=remove)
        
