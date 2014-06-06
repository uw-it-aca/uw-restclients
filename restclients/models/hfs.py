from django.db import models
from restclients.util.formator import truncate_time_str


def hfs_account_json_data(account, older_than_days_to_omit_time=0):
    return {
        'balance': account.balance,
        'last_updated': truncate_time_str(account.last_updated,
                                          older_than_days_to_omit_time),
        'add_funds_url': account.add_funds_url
        }


def hfs_account_str(account):
    return "{last_updated: %s, balance: %.2f, add_funds_url: %s}" % (
        account.last_updated, account.balance, account.add_funds_url)


class StudentHuskyCardAccout(models.Model):
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    last_updated = models.DateTimeField()
    add_funds_url = models.CharField(max_length=80)


    def json_data(self, older_than_days_to_omit_time=0):
        return hfs_account_json_data(self, older_than_days_to_omit_time)


    def __str__(self):
        return hfs_account_str(self)


class EmployeeHuskyCardAccount(models.Model):
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    last_updated = models.DateTimeField()
    add_funds_url = models.CharField(max_length=80)


    def json_data(self, older_than_days_to_omit_time=0):
        return hfs_account_json_data(self, older_than_days_to_omit_time)


    def __str__(self):
        return hfs_account_str(self)


class ResidentDiningAccount(models.Model):
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    last_updated = models.DateTimeField()
    add_funds_url = models.CharField(max_length=80)


    def json_data(self, older_than_days_to_omit_time=0):
        return hfs_account_json_data(self, older_than_days_to_omit_time)


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


    def json_data(self, older_than_days_to_omit_time=0):
        return_value = {
            'student_husky_card': None,
            'employee_husky_card': None,
            'resident_dining': None
            }

        if self.student_husky_card is not None:
            return_value['student_husky_card'] = self.student_husky_card.json_data(
                older_than_days_to_omit_time)

        if self.employee_husky_card is not None:
            return_value['employee_husky_card'] = self.employee_husky_card.json_data(
                older_than_days_to_omit_time)

        if self.resident_dining is not None:
            return_value['resident_dining'] = self.resident_dining.json_data(
                older_than_days_to_omit_time)

        return return_value


