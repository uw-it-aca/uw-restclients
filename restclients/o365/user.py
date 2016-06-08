"""
Provides Office 365 graph web API User Operations
See: https://msdn.microsoft.com/en-us/library/azure/ad/graph/api/users-operations
"""  # noqa
from restclients.o365 import O365
from restclients.models.o365 import User as UserModel
from urlparse import urlparse, parse_qs


class User(O365):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._per_page = None
        if 'per_page' in kwargs:
            self._per_page = kwargs['per_page']

    def get_users(self, params=None):
        all_users = []
        url = '/users'
        while url:
            users, nextlink = self._get_users_from_url(url, params=params)
            all_users.extend(users)
            url, params = self._next_page(nextlink, params)

        return all_users

    def get_users_generator(self, params=None, formatter=None):
        url = '/users'
        while url:
            users, nextlink = self._get_users_from_url(url, params=params)
            for user in users:
                yield formatter(user) if formatter else user

            url, params = self._next_page(nextlink, params)

    def _get_users_from_url(self, url, params=None):
        data = self.get_resource(url, params=self._params(params))
        users = []
        for user_data in data.get('value', []):
            users.append(UserModel().from_json(user_data))

        nextlink = data['odata.nextLink'] if 'odata.nextLink' in data else None
        return users, nextlink

    def _next_page(self, nextlink, params=None):
        url = None
        if nextlink:
            parsed_url = urlparse(nextlink)
            qs = parse_qs(parsed_url.query)
            if '$skiptoken' in qs:
                url = "/%s" % parsed_url.path
                if not params:
                    params = {}

                params['$skiptoken'] = qs['$skiptoken'][0]

        return url, params

    def _params(self, params):
        if not params:
            params = {}

        if self._per_page:
            params['$top'] = self._per_page

        return params

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
