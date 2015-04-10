from django.db import models


class Evaluation(models.Model):
    section_sln = models.IntegerField(max_length=5)
    instructor_id = models.IntegerField(max_length=9)
    eval_open_date = models.DateTimeField()
    eval_close_date = models.DateTimeField()
    eval_status = models.CharField(max_length=7)
    eval_is_online = models.BooleanField(default=False)
    eval_url = models.URLField()
