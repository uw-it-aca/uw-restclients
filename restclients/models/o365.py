from django.db import models
from dateutil.parser import parse as date_parse


# Office365 User
class User(models.Model):
    object_id = models.CharField(max_length=36)
    immutable_id = models.CharField(max_length=32, null=True)
    user_type = models.CharField(max_length=16, null=True)
    account_enabled = models.NullBooleanField()
    dir_sync_enabled = models.NullBooleanField()
    user_principal_name = models.CharField(max_length=128, null=True)
    job_title = models.CharField(max_length=32, null=True)
    mail = models.CharField(max_length=128, null=True)
    mail_nick_name = models.CharField(max_length=128, null=True)
    display_name = models.CharField(max_length=32, null=True)
    given_name = models.CharField(max_length=32, null=True)
    surname = models.CharField(max_length=32, null=True)
    department = models.CharField(max_length=36, null=True)
    last_dir_sync_time = models.TimeField()
    object_type = models.CharField(max_length=16, null=True)
    street_address = models.CharField(max_length=256, null=True)
    state = models.CharField(max_length=32, null=True)
    postal_code = models.CharField(max_length=16, null=True)
    country = models.CharField(max_length=32, null=True)
    physical_delivery_office_name = models.CharField(max_length=64, null=True)
    telephone_number = models.CharField(max_length=32, null=True)
    mobile = models.CharField(max_length=32, null=True)
    password_policies = models.CharField(max_length=32, null=True)
    preferred_language = models.CharField(max_length=32, null=True)

    def from_json(self, data):
        self.object_id = data.get('objectId')
        self.immutable_id = data.get('immutableId')
        self.user_type = data.get('userType')
        self.account_enabled = data.get('accountEnabled')
        self.dir_sync_enabled = data.get('dirSyncEnabled')
        self.user_principal_name = data.get('userPrincipalName')
        self.mail_nick_name = data.get('mailNickname')
        self.job_title = data.get('jobTitle')
        self.department = data.get('department')
        self.mail = data.get('mail')
        self.surname = data.get('surname')
        self.given_name = data.get('givenName')
        self.last_dir_sync_time = date_parse(data.get('lastDirSyncTime'))
        self.object_type = data.get('objectType')
        self.street_address = data.get('streetAddress')
        self.state = data.get('state')
        self.postal_code = data.get('postalCode')
        self.country = data.get('country')
        self.physical_delivery_office_name = data.get('physicalDeliveryOfficeName')
        self.telephone_number = data.get('telephoneNumber')
        self.mobile = data.get('mobile')
        self.password_policies = data.get('passwordPolicies')
        self.display_name = data.get('displayName')
        self.preferred_language = data.get('preferredLanguage')
        
        self.assigned_licenses = []
        for license_data in data.get('assignedLicenses', []):
            self.assigned_licenses.append(License().from_json(license_data))

        self.assigned_plans = []
        for plan in data.get('assignedPlans', []):
            self.assigned_plans.append(ServicePlan().from_json(plan))

        self.provisioned_plans = []
        for plan in data.get('provisionedPlans', []):
            self.provisioned_plans.append(Plan().from_json(plan))

        self.other_mails = []
        for mail in data.get('otherMails', []):
            self.other_mails.append(Mail().from_json(mail))

        self.proxy_addresses = []
        for addr in data.get('proxyAddresses', []):
            self.proxy_addresses.append("%s" % addr)

        self.provisioning_errors = []
        for err in data.get('provisioningErrors', []):
            self.provisioning_errors.append("%s" % err)

        return self


class License(models.Model):
    sku_id = models.CharField(max_length=36)

    def from_json(self, data):
        self.sku_id = data.get('skuId')
        self.disabled_plans = []
        for disabled in data.get('disabledPlans', []):
            self.disabled_plans.append(disabled)

        return self

    def json_data(self):
        data = {
            'skuId': self.sku_id
        }

        data[disabledPlans] = []
        for plan in self.disabled_plans:
            data['disabledPlans'].append(plan.json_data())

        return data


class Mail(models.Model):
    mail = models.CharField(max_length=256, null=True)

    def _json_to_mail(self, data):
        return Mail(mail=data)


class Plan(models.Model):
    sku_id = models.CharField(max_length=36)

    def from_json(self, data):
        self.sku_id = data.get('skuId')

        self.disabled_plans = []
        for plan in data.get('disabledPlans', []):
            self.disabled_plans.append(plan)

        return self


class PrepaidUnits(models.Model):
    warning = models.PositiveSmallIntegerField()
    enabled = models.PositiveSmallIntegerField()
    suspended = models.PositiveSmallIntegerField()

    def from_json(self, data):
        self.warning = int(data.get('warning'))
        self.enabled = int(data.get('enabled'))
        self.suspended = int(data.get('suspended'))

        return self


class SKU(models.Model):
    sku_id = models.CharField(max_length=36)
    sku_part_number = models.CharField(max_length=128, null=True)
    object_id = models.CharField(max_length=128, null=True)
    capability_status = models.CharField(max_length=16, null=True)
    consumed_units = models.PositiveSmallIntegerField()
    capability_status = models.CharField(max_length=16, null=True)
    prepaid_units = models.ForeignKey(PrepaidUnits, on_delete=models.PROTECT)

    def from_json(self, data):
        self.sku_id = data.get('skuId')
        self.sku_part_number = data.get('skuPartNumber')
        self.capability_status = data.get('capabilityStatus')
        self.object_id = data.get('objectId')
        self.consumed_units = int(data.get('consumedUnits'))
        self.capability_status = data.get('capabilityStatus')
        self.prepaid_units = PrepaidUnits().from_json(data.get('prepaidUnits'))

        self.service_plans = []
        for plan in data.get('servicePlans', []):
            self.service_plans.append(ServicePlan().from_json(plan))

        return self


class ServicePlan(models.Model):
    service = models.CharField(max_length=64)
    service_plan_id = models.CharField(max_length=36)
    service_plan_name = models.CharField(max_length=64, null=True)
    capability_status = models.CharField(max_length=16, null=True)
    assigned_timestamp = models.TimeField(null=True)

    def from_json(self, data):
        self.service=data.get('service')
        self.capability_status = data.get('capabilityStatus')
        self.service_plan_id = data.get('servicePlanId')
        self.service_plan_name = data.get('servicePlanName')
        self.assigned_timestamp = date_parse(data['assignedTimestamp']) if 'assignedTimestamp' in data else None
        return self
