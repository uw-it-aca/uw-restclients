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

    def parent(self):
        if not hasattr(self, "_parent"):
            self._parent = None
            if self.parent_id is not None:
                from restclients.r25.events import get_event_by_id
                self._parent = get_event_by_id(self.parent_id)
        return self._parent

    def children(self):
        if not hasattr(self, "_children"):
            from restclients.r25.events import get_events
            self._children = get_events(parent_id=self.event_id)
        return self._children

    def cabinet(self):
        if self.cabinet_id is not None:
            if self.cabinet_id == self.event_id:
                return self
            else:
                from restclients.r25.events import get_event_by_id
                return get_event_by_id(self.cabinet_id)

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
    event_id = models.IntegerField(max_length=10)
    event_name = models.CharField(max_length=64)
    profile_name = models.CharField(max_length=32)
    contact_name = models.CharField(max_length=64)
    contact_email = models.CharField(max_length=64)

    def state_name(self):
        return dict(self.STATE_CHOICES)[self.state]

    class Meta:
        db_table = "restclients_r25_reservation"


class BindingReservation(models.Model):
    bound_reservation_id = models.IntegerField(max_length=10)
    primary_reservation = models.IntegerField(max_length=10)
    name = models.CharField(max_length=200)
    bound_event_id = models.IntegerField(max_length=10)

    class Meta:
        db_table = "restclients_r25_binding_reservation"
