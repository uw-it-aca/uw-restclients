import json
from datetime import datetime
from django.db import models


class BridgeCustomField(models.Model):
    REGID_FIELD_ID = "5"
    REGID_NAME = "REGID"

    value_id = models.CharField(max_length=10, null=True, default=None)
    field_id = models.CharField(max_length=10)
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=256, null=True, default=None)

    def is_regid(self):
        return self.name == BridgeCustomField.REGID_NAME

    def __str__(self):
        return "{%s: %s, %s: %s, %s: %s, %s: %s}" % (
            'value_id', self.value_id,
            'id', self.field_id,
            'name', self.name,
            'value', self.value
            )

    def to_json(self):
        value = {"custom_field_id": self.field_id,
                 "value": self.value
                 }
        if self.value_id:
            value["id"] = self.value_id
        return value

    class Meta:
        db_table = "restclients_bridge_custom_field"


class BridgeUser(models.Model):
    bridge_id = models.IntegerField(default=0)
    netid = models.CharField(max_length=32)
    email = models.CharField(max_length=128)
    full_name = models.CharField(max_length=256)
    first_name = models.CharField(max_length=128, null=True, default=None)
    last_name = models.CharField(max_length=128, null=True, default=None)
    name = models.CharField(max_length=256, null=True, default=None)
    sortable_name = models.CharField(max_length=256, null=True, default=None)
    avatar_url = models.CharField(max_length=512, null=True, default=None)
    locale = models.CharField(max_length=2, default='en')
    logged_in_at = models.DateTimeField(null=True, default=None)
    updated_at = models.DateTimeField(null=True, default=None)
    unsubscribed = models.CharField(max_length=128, null=True, default=None)
    next_due_date = models.DateTimeField(null=True, default=None)
    completed_courses_count = models.IntegerField(default=0)

    def get_uid(self):
        return "%s@uw.edu" % self.netid

    def to_json_post(self):
        # for POST, PATCH
        custom_fields_json = []
        for field in self.custom_fields:
            custom_fields_json.append(field.to_json())

        ret_user = {"uid": self.get_uid(),
                    "full_name": self.full_name,
                    "email": self.email,
                    "custom_fields": custom_fields_json
                    }
        if self.first_name:
            ret_user["first_name"] = self.first_name
        if self.last_name:
            ret_user["last_name"] = self.last_name
        return {"users": [ret_user]}

    def __str__(self):
        return ("{%s: %d, %s: %s, %s: %s, %s: %s, %s: %s, %s: %s," +
                " %s: %s, %s: %s, %s: %s, %s: %s, %s: %d}") % (
                "bridge_id", self.bridge_id,
                "netid", self.netid,
                "first_name", self.first_name,
                "last_name", self.last_name,
                "full_name", self.full_name,
                "sortable_name", self.sortable_name,
                "name", self.name,
                "email", self.email,
                "updated_at", self.updated_at,
                "logged_in_at", self.logged_in_at,
                "completed_courses_count", self.completed_courses_count)

    def __init__(self):
        self.roles = []
        self.custom_fields = []

    class Meta:
        db_table = "restclients_bridge_user"


class BridgeUserRole(models.Model):
    role_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)

    def __init__(self):
        self.permissions = []

    def to_json(self):
        return {
            "id": self.role_id,
            "name": self.name,
            "permissions": self.permissions  # unknown
            }

    class Meta:
        db_table = "restclients_bridge_user_role"
