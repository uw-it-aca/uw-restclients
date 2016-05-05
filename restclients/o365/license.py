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

    def set_user_licenses(self, user, add=None, remove=None):
        """Implements: assignLicense
        https://msdn.microsoft.com/library/azure/ad/graph/api/functions-and-actions#assignLicense

        "add" is a dictionary of licence sku id's that reference an
        array of disabled plan id's
             add = { '<license-sku-id>': ['<disabled-plan-id'>, ...]
        "remove" is an array of license sku id's
             remove = ['<license-sku-id'>, ...]

        """  # noqa
        url = '/users/%s/assignLicense' % (user)
        add_licenses = []
        if add:
            for l in add:
                add_licenses.append({
                    'skuId': l,
                    'disabledPlans': add[l]
                })

        body = {
            'addLicenses': add_licenses,
            'removeLicenses': remove if remove else []
        }

        data = self.post_resource(url, json=body)
        return data

    def set_licenses_for_netid(self, netid, add=None,
                               remove=None, domain='test'):
        return self.set_user_licenses(
            self.user_principal(netid, domain), add=add, remove=remove)
