import json
from restclients_core import models


CURRENT = "U-PASS Membership is current."
STUDENT = "Your Student U-PASS Membership "
EMPLOYEE = "Your Faculty/Staff U-PASS Membership "


class UPassStatus(models.Model):
    status_message = models.TextField()
    is_current = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def json_data(self):
        data = {
            'status_message': self.status_message,
            'is_current': self.is_current,
            'is_employee': self.is_employee,
            'is_student': self.is_student,
        }
        return data

    @classmethod
    def create(cls, status_data):
        status = cls(status_message=status_data)
        if CURRENT in status_data:
            status.is_current = True

        if STUDENT in status_data:
            status.is_student = True

        if EMPLOYEE in status_data:
            status.is_employee = True
        return status

    def __str__(self):
        return json.dumps(self.json_data())
