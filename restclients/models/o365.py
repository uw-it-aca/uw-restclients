from restclients_core import models
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
    last_dir_sync_time = models.TimeField(null=True)
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
        self.object_type = data.get('objectType')
        self.street_address = data.get('streetAddress')
        self.state = data.get('state')
        self.postal_code = data.get('postalCode')
        self.country = data.get('country')
        self.physical_delivery_office_name = data.get(
            'physicalDeliveryOfficeName')
        self.telephone_number = data.get('telephoneNumber')
        self.mobile = data.get('mobile')
        self.password_policies = data.get('passwordPolicies')
        self.display_name = data.get('displayName')
        self.preferred_language = data.get('preferredLanguage')

        last_dir_sync = data.get('lastDirSyncTime')
        self.last_dir_sync_time = date_parse(
            last_dir_sync) if last_dir_sync else None

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

    def json_data(self):
        json_data = {
            'object_id': self.object_id,
            'immutable_id': self.immutable_id,
            'user_type': self.user_type,
            'account_enabled': self.account_enabled,
            'dir_sync_enabled': self.dir_sync_enabled,
            'user_principal_name': self.user_principal_name,
            'mail_nick_name': self.mail_nick_name,
            'job_title': self.job_title,
            'department': self.department,
            'mail': self.mail,
            'surname': self.surname,
            'given_name': self.given_name,
            'last_dir_sync_time': self.last_dir_sync_time.isoformat(),
            'object_type': self.object_type,
            'street_address': self.street_address,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'physical_delivery_office_name': getattr(
                self, 'physical_delivery_office_name'),
            'telephone_number': self.telephone_number,
            'mobile': self.mobile,
            'password_policies': self.password_policies,
            'display_name': self.display_name,
            'preferred_language': self.preferred_language
        }

        json_data['assigned_licenses'] = []
        for license_data in self.assigned_licenses:
            json_data['assigned_licenses'].append(license_data.json_data())

        json_data['assigned_plans'] = []
        for plan in self.assigned_plans:
            json_data['assigned_plans'].append(plan.json_data())

        json_data['provisioned_plans'] = []
        for plan in self.provisioned_plans:
            json_data['provisioned_plans'].append(plan.json_data())

        json_data['other_mails'] = []
        for mail in self.other_mails:
            json_data['other_mails'].append(mail)

        json_data['proxy_addresses'] = []
        for addr in self.proxy_addresses:
            json_data['proxy_addresses'].append("%s" % addr)

        json_data['provisioning_errors'] = []
        for err in self.provisioning_errors:
            json_data['provisioning_errors'].append("%s" % err)

        return json_data


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

        data['disabledPlans'] = []
        for plan in self.disabled_plans:
            data['disabledPlans'].append(plan)

        return data


class Mail(models.Model):
    mail = models.CharField(max_length=256, null=True)

    def from_json(self, data):
        return Mail(mail=data)

    def json_data(self):
        return self.mail


class Plan(models.Model):
    sku_id = models.CharField(max_length=36)

    def from_json(self, data):
        self.sku_id = data.get('skuId')

        self.disabled_plans = []
        for plan in data.get('disabledPlans', []):
            self.disabled_plans.append(plan)

        return self

    def json_data(self):
        return self.sku_id


class PrepaidUnits(models.Model):
    warning = models.PositiveSmallIntegerField()
    enabled = models.PositiveSmallIntegerField()
    suspended = models.PositiveSmallIntegerField()

    def from_json(self, data):
        self.warning = int(data.get('warning'))
        self.enabled = int(data.get('enabled'))
        self.suspended = int(data.get('suspended'))
        return self

    def json_data(self):
        return {
            'warning': self.warning,
            'enabled': self.enabled,
            'suspended': self.suspended
        }


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

    def json_data(self):
        json_data = {
            'sku_id': self.sku_id,
            'sku_part_number': self.sku_part_number,
            'capability_status': self.capability_status,
            'object_id': self.object_id,
            'consumed_units': self.consumed_units,
            'capability_status': self.capability_status,
            'prepaid_units': self.prepaid_units.json_data()
        }

        json_data['service_plans'] = []
        for plan in self.service_plans:
            json_data['service_plans'].append(self.service_plans.json_data())

        return json_data


class ServicePlan(models.Model):
    service = models.CharField(max_length=64)
    service_plan_id = models.CharField(max_length=36)
    service_plan_name = models.CharField(max_length=64, null=True)
    capability_status = models.CharField(max_length=16, null=True)
    assigned_timestamp = models.TimeField(null=True)

    def from_json(self, data):
        self.service = data.get('service')
        self.capability_status = data.get('capabilityStatus')
        self.service_plan_id = data.get('servicePlanId')
        self.service_plan_name = data.get('servicePlanName')
        self.assigned_timestamp = date_parse(data['assignedTimestamp']) \
            if 'assignedTimestamp' in data else None

        return self

    def json_data(self):
        return {
            'service': self.service,
            'capability_status': self.capability_status,
            'service_plan_id': self.service_plan_id,
            'service_plan_name': self.service_plan_name,
            'assigned_timestamp': self.assigned_timestamp.isoformat()
        }
