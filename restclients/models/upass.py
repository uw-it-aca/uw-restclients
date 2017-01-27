from django.db import models


class UPassStatus(models.Model):
    status_message = models.TextField()
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def json_data(self):
        data = {
            'status_message': self.status_message,
            'is_active': self.is_active,
            'is_staff': self.is_staff,
            'is_student': self.is_student,
        }
        return data

    @classmethod
    def create(cls, status_data):
        status = cls(status_message=status_data)
        if "Student" in status_data:
            status.is_student = True
            status.is_active = True
        elif "Faculty" in status_data:
            status.is_staff = True
            status.is_active = True
        return status
