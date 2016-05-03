"""
Provides Office 365 graph web API User Operations
See: https://msdn.microsoft.com/en-us/library/azure/ad/graph/api/users-operations
"""
from django.conf import settings
from restclients.o365 import O365
from restclients.models.o365 import User as UserModel


class User(O365):
    def get_user(self, user):
        url = '/users/%s' % (user)
        data = self.get_resource(url)
        return UserModel().from_json(data)

    def get_user_by_netid(self, netid, domain='test'):
        user = '%s@%s' % (
            netid, getattr(settings, 'RESTCLIENTS_O365_PRINCIPLE_DOMAIAN', domain))
        return self.get_user(user)
