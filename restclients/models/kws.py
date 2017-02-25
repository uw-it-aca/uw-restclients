from restclients_core import models


class Key(models.Model):
    algorithm = models.CharField(max_length=100)
    cipher_mode = models.CharField(max_length=100)
    expiration = models.DateTimeField()
    key_id = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    size = models.SmallIntegerField()
    url = models.CharField(max_length=1000)
