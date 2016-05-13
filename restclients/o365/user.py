"""
Provides Office 365 graph web API User Operations
See: https://msdn.microsoft.com/en-us/library/azure/ad/graph/api/users-operations
"""  # noqa
from django.conf import settings
from restclients.o365 import O365
from restclients.models.o365 import User as UserModel


class User(O365):
    def get_user(self, user):
        url = '/users/%s' % (user)
        data = self.get_resource(url)
        return UserModel().from_json(data)

    def get_user_by_netid(self, netid, domain='test'):
        return self.get_user(self.user_principal(netid, domain))

    def get_user_property(self, user, property):
        url = '/users/%s/%s' % (user, property)
        data = self.get_resource(url)
        return data.get('value', '')

    def get_property_for_netid(self, netid, property, domain='test'):
        return self.get_user_property(
            self.user_principal(netid, domain), property)

    def set_user_property(self, user, property, new_value):
        url = '/users/%s/%s' % (user, property)
        data = self.patch_resource(url, json={'value': new_value})
        return data.get('value', '')

    def set_property_for_netid(self, netid, property,
                               new_value, domain='test'):
        return self.set_user_property(
            self.user_principal(netid, domain), property, new_value)

    def get_user_location(self, user):
        return self.get_user_property(user, 'usageLocation')

    def get_location_for_netid(self, netid, domain='test'):
        return self.get_property_for_netid(
            netid, 'usageLocation', domain=domain)

    def set_user_location(self, user, location):
        return self.set_user_property(user, 'usageLocation', location)

    def set_location_for_netid(self, netid, location, domain='test'):
        return self.set_property_for_netid(netid, 'usageLocation',
                                           location, domain=domain)
