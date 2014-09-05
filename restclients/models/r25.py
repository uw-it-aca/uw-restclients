from django.db import models


class Space(models.Model):
    space_id = models.IntegerField(max_length=10)
    name = models.CharField(max_length=100)
    formal_name = models.CharField(max_length=200)

    class Meta:
        db_table = "restclients_r25_space"
