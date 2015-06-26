from django.db import models


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
