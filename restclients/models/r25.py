from django.db import models


class Event(models.Model):
    DRAFT_STATE = "0"
    TENTATIVE_STATE = "1"
    CONFIRMED_STATE = "2"
    SEALED_STATE = "3"
    DENIED_STATE = "4"
    CANCELLED_STATE = "99"

    STATE_CHOICES = (
        (DRAFT_STATE, "Draft"),
        (TENTATIVE_STATE, "Tentative"),
        (CONFIRMED_STATE, "Confirmed"),
        (SEALED_STATE, "Sealed"),
        (DENIED_STATE, "Denied"),
        (CANCELLED_STATE, "Cancelled"),
    )

    event_id = models.IntegerField(max_length=10)
    alien_uid = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    parent_id = models.IntegerField(max_length=10, null=True)
    cabinet_id = models.IntegerField(max_length=10, null=True)
    cabinet_name = models.CharField(max_length=100, null=True)

    def state_name(self):
        return dict(self.STATE_CHOICES)[self.state]

    class Meta:
        db_table = "restclients_r25_event"


class Space(models.Model):
    space_id = models.IntegerField(max_length=10)
    name = models.CharField(max_length=100)
    formal_name = models.CharField(max_length=200)

    class Meta:
        db_table = "restclients_r25_space"


class Reservation(models.Model):
    STANDARD_STATE = "1"
    EXCEPTION_STATE = "2"
    WARNING_STATE = "3"
    OVERRIDE_STATE = "4"
    CANCELLED_STATE = "99"

    STATE_CHOICES = (
        (STANDARD_STATE, "Standard"),
        (EXCEPTION_STATE, "Exception"),
        (WARNING_STATE, "Warning"),
        (OVERRIDE_STATE, "Override"),
        (CANCELLED_STATE, "Cancelled"),
    )

    reservation_id = models.IntegerField(max_length=10)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def state_name(self):
        return dict(self.STATE_CHOICES)[self.state]

    class Meta:
        db_table = "restclients_r25_reservation"
