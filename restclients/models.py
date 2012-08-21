from django.db import models

class Person(models.Model):
    uwregid = models.CharField(max_length=32,
                               db_index=True,
                               unique=True)

    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)

class Term(models.Model):
    year = models.PositiveSmallIntegerField()
    QUARTERNAME_CHOICES = (
        ('1', 'Winter'),
        ('2', 'Spring'),
        ('3', 'Summer'),
        ('4', 'Fall')
        )
    quarter = models.CharField(max_length=1,
                               choices=QUARTERNAME_CHOICES)
    first_day_quarter = models.DateField(db_index=True)
    last_day_instruction = models.DateField(db_index=True)
    aterm_last_date = models.DateField()
    bterm_first_date = models.DateField()
    last_final_exam_date = models.DateField()
    class Meta:
        unique_together = ('year',
                           'quarter')
