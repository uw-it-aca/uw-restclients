from django.db import models


class Evaluation(models.Model):
    section_sln = models.IntegerField(max_length=5)
    eval_open_date = models.DateTimeField()
    eval_close_date = models.DateTimeField()
    eval_status = models.CharField(max_length=7)
    eval_is_online = models.BooleanField(default=False)
    eval_url = models.URLField()

    def __init__(self, *args, **kwargs):
        super(Evaluation, self).__init__(*args, **kwargs)
        self.instructor_ids = []


    def __str__(self):
        return "{sln: %d, eval_is_online: %s, status: %s}" % (
            self.section_sln, self.eval_is_online, self.eval_status)
