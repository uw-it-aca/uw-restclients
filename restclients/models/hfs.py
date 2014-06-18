from django.db import models
from restclients.util.date_formator import past_datetime_str


def get_timestamp_str(last_updated_datetime, use_custom_date_format):
    if use_custom_date_format:
        return past_datetime_str(last_updated_datetime)
    else:
        return str(last_updated_datetime)


def hfs_account_json_data(account, use_custom_date_format):
    return {
        'balance': account.balance,
        'last_updated': get_timestamp_str(account.last_updated,
                                          use_custom_date_format),
        'add_funds_url': account.add_funds_url
        }


def hfs_account_str(account):
    return "{last_updated: %s, balance: %.2f, add_funds_url: %s}" % (
        account.last_updated, account.balance, account.add_funds_url)


class StudentHuskyCardAccout(models.Model):
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    last_updated = models.DateTimeField()
    add_funds_url = models.CharField(max_length=80)


    def json_data(self, use_custom_date_format=False):
        return hfs_account_json_data(self, use_custom_date_format)


    def __str__(self):
        return hfs_account_str(self)


class EmployeeHuskyCardAccount(models.Model):
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    last_updated = models.DateTimeField()
    add_funds_url = models.CharField(max_length=80)


    def json_data(self, use_custom_date_format=False):
        return hfs_account_json_data(self, use_custom_date_format)


    def __str__(self):
        return hfs_account_str(self)


class ResidentDiningAccount(models.Model):
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    last_updated = models.DateTimeField()
    add_funds_url = models.CharField(max_length=80)


    def json_data(self, use_custom_date_format=False):
        return hfs_account_json_data(self, use_custom_date_format)


    def __str__(self):
        return hfs_account_str(self)


class HfsAccouts(models.Model):
    student_husky_card = models.ForeignKey(StudentHuskyCardAccout,
                                           on_delete=models.PROTECT,
                                           null=True, default=None)
    employee_husky_card = models.ForeignKey(EmployeeHuskyCardAccount,
                                           on_delete=models.PROTECT,
                                           null=True, default=None)
    resident_dining = models.ForeignKey(ResidentDiningAccount,
                                        on_delete=models.PROTECT,
                                        null=True, default=None)


    def json_data(self, use_custom_date_format=False):
        return_value = {
            'student_husky_card': None,
            'employee_husky_card': None,
            'resident_dining': None
            }

        if self.student_husky_card is not None:
            return_value['student_husky_card'] = self.student_husky_card.json_data(
                use_custom_date_format)

        if self.employee_husky_card is not None:
            return_value['employee_husky_card'] = self.employee_husky_card.json_data(
                use_custom_date_format)

        if self.resident_dining is not None:
            return_value['resident_dining'] = self.resident_dining.json_data(
                use_custom_date_format)

        return return_value


