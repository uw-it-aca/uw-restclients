from django.db import models
from restclients.models.base import RestClientsModel


class UwEmailForwarding(models.Model):
    fwd = models.CharField(max_length=64, null=True)
    permitted = models.NullBooleanField()
    status = models.CharField(max_length=16)

    def is_active(self):
        return self.status == "Active"

    def is_uwgmail(self):
        return self.fwd is not None and "@gamail.uw.edu" in self.fwd

    def is_uwlive(self):
        return self.fwd is not None and "@ol.uw.edu" in self.fwd

    def json_data(self):
        return {'fwd': self.fwd,
                'status': self.status,
                'is_active': self.is_active(),
                'permitted': self.permitted,
                'is_uwgmail': self.is_uwgmail(),
                'is_uwlive': self.is_uwlive()
                }

    def __str__(self):
        return "{status: %s, permitted: %s, fwd: %s}" % (
            self.status, self.permitted, self.fwd)


class Subscription(RestClientsModel):
    STATUS_ACTIVE = 20
    STATUS_EXPIRED = 21
    STATUS_DISUSERED = 22
    STATUS_PENDING = 23
    STATUS_INACTIVE = 24
    STATUS_CANCELLING = 25
    STATUS_SUSPENDED = 29
    STATUS_UNPERMITTED = 101

    STATUS_CHOICES = (
        (STATUS_ACTIVE, "Active"),
        (STATUS_EXPIRED, "Expired"),
        (STATUS_DISUSERED, "Disusered"),
        (STATUS_PENDING, "Pending"),
        (STATUS_INACTIVE, "Inactive"),
        (STATUS_CANCELLING, "Cancelling"),
        (STATUS_SUSPENDED, "Suspended"),
        (STATUS_UNPERMITTED, "Unpermitted"),
    )

    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)
    subscription_code = models.SmallIntegerField()
    subscription_name = models.CharField(max_length=64)
    permitted = models.BooleanField(default=False)
    status_code = models.SmallIntegerField(choices=STATUS_CHOICES)
    status_name = models.CharField(max_length=12)
    data_value = models.CharField(max_length=32, null=True)
    data_field = models.CharField(max_length=256, null=True)

    def __init__(self, *args, **kwargs):
        super(Subscription, self).__init__(*args, **kwargs)
        self.actions = []
        self.permits = []

    def from_json(self, uwnetid, data):
        self.uwnetid = uwnetid
        self.subscription_code = int(data['subscriptionCode'])
        self.subscription_name = data['subscriptionName']
        self.permitted = data['permitted']
        self.status_code = int(data['statusCode'])
        self.status_name = data['statusName']

        if 'dataField' in data:
            self.data_field = data['dataField']

        if 'dataValue' in data:
            self.data_value = data['dataValue']

        for action_data in data.get('actions', []):
            action = SubscriptionAction(
                action=action_data)
            self.actions.append(action)

        for permit_data in data.get('permits', []):
            permit = SubscriptionPermit(
                mode=permit_data['mode'],
                category_code=permit_data['categoryCode'],
                category_name=permit_data['categoryName'],
                status_code=permit_data['statusCode'],
                status_name=permit_data['statusName'])

            if 'dataValue' in permit_data:
                permit.data_value = permit_data['dataValue']

            self.permits.append(permit)

        return self

    def json_data(self):
        data = {
            'uwNetID': self.uwnetid,
            'subscriptionCode': self.subscription_code,
            'subscriptionName': self.subscription_name,
            'permitted': self.permitted,
            'statusCode': self.status_code,
            'statusName': self.status_name,
            'actions': [],
            'permits': []
        }

        if self.data_field:
            data['dataField'] = self.data_field

        if self.data_value:
            data['dataValue'] = self.data_value

        for action in self.actions:
            data['actions'].append(action.json_data())

        for permit in self.permits:
            data['permits'].append(permit.json_data())

        return data

    def __str__(self):
        return "{netid: %s, %s: %s, %s: %s, status_name: %s}" % (
            self.uwnetid, "subscription_code", self.subscription_code,
            "status_code", self.status_code, self.status_name)


class SubscriptionPermit(RestClientsModel):
    STAFF_CATEGORY_CODE = 4
    FACULTY_CATEGORY_CODE = 5
    CURRENT_STATUS_CODE = 1
    IMPLICIT_MODE = "implicit"

    mode = models.CharField(max_length=16)
    category_code = models.SmallIntegerField()
    category_name = models.CharField(max_length=32)
    status_code = models.SmallIntegerField()
    status_name = models.CharField(max_length=16)
    data_value = models.CharField(max_length=256, null=True)

    def is_mode_implicit(self):
        return self.mode == SubscriptionPermit.IMPLICIT_MODE

    def is_category_staff(self):
        return self.category_code == SubscriptionPermit.STAFF_CATEGORY_CODE

    def is_category_faculty(self):
        return self.category_code == SubscriptionPermit.FACULTY_CATEGORY_CODE

    def is_status_current(self):
        return self.status_code == SubscriptionPermit.CURRENT_STATUS_CODE

    def json_data(self):
        data = {
            'type': 'permit',
            'mode': mode,
            'categoryCode': category_code,
            'categoryName': category_name,
            'statusCode': status_code,
            'statusName': status_name,
        }

        if data_value:
            data['dataValue'] = data_value

        return data


class SubscriptionAction(RestClientsModel):
    SHOW = "show"
    ACTIVATE = "activate"
    DEACTIVATE = "deactivate"
    SUSPEND = "suspend"
    REACTIVATE = "reactivate"
    MODIFY = "modify"
    SETNAME = "setname"
    DISUSER = "disuser"
    REUSE = "reuse"

    ACTION_TYPES = (
        (SHOW, "Show"),
        (ACTIVATE, "Activate"),
        (DEACTIVATE, "Deactivate"),
        (SUSPEND, "Suspend"),
        (REACTIVATE, "Reactivate"),
        (MODIFY, "Modify"),
        (SETNAME, "Setname"),
        (DISUSER, "Disuser"),
        (REUSE, "Reuse"),
    )

    action = models.CharField(max_length=12,
                              choices=ACTION_TYPES,
                              default=SHOW)

    def json_data(self):
        return action
