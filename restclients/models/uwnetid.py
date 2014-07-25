from django.db import models

class UwEmailForwarding(models.Model):
    fwd = models.CharField(max_length=64, null=True)
    permitted = models.BooleanField()
    status = models.CharField(max_length=16)

    def is_active(self):
        return self.status == "Active"

    def json_data(self):
        return {'fwd': self.fwd,
                'status': self.status,
                'permitted': self.permitted
                }

    def __str__(self):
        return "{status: %s, permitted: %s, fwd: %s}" % (
            self.status, self.permitted, self.fwd)
