from django.db import models


class Evaluation(models.Model):
    section_sln = models.IntegerField(max_length=5)
    eval_open_date = models.DateTimeField()
    eval_close_date = models.DateTimeField()
    eval_status = models.CharField(max_length=7)
    eval_url = models.URLField()

    def __init__(self, *args, **kwargs):
        super(Evaluation, self).__init__(*args, **kwargs)
        self.instructor_ids = []


    def __str__(self):
        return "{%s: %d, %s: %s, %s: %s, %s: %s}" % (
            "sln", self.section_sln,
            "eval_open_date", self.eval_open_date,
            "eval_close_date", self.eval_close_date,
            "eval_url", self.eval_url)
