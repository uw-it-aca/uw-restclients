import json
from datetime import datetime
from django.db import models


class BridgeCustomField(models.Model):
    REGID_FIELD_ID = "5"
    REGID_NAME = "regid"

    value_id = models.CharField(max_length=10, null=True, default=None)
    field_id = models.CharField(max_length=10)
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=256, null=True, default=None)

    def is_regid(self):
        return self.name.lower() == BridgeCustomField.REGID_NAME

    def to_json(self):
        value = {'custom_field_id': self.field_id,
                 'value': self.value,
                 }
        try:
            if self.value_id:
                value['id'] = self.value_id
        except AttributeError:
            pass
        return value

    def __init__(self, *args, **kwargs):
        super(BridgeCustomField, self).__init__(*args, **kwargs)

    def __str__(self):
        data = self.to_json()
        data["name"] = self.name
        return json.dumps(data)

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
    completed_courses_count = models.IntegerField(default=-1)

    def get_uid(self):
        return "%s@uw.edu" % self.netid

    def has_course_summary(self):
        try:
            return self.completed_courses_count >= 0
        except AttributeError:
            return False

    def has_bridge_id(self):
        return self.bridge_id > 0

    def no_learning_history(self):
        return self.has_course_summary() and self.completed_courses_count == 0

    def json_data(self, omit_custom_fields=False):
        # omit_custom_fields if it is empty
        ret_user = {"uid": self.get_uid(),
                    "full_name": self.full_name,
                    "email": self.email,
                    }
        if not (len(self.custom_fields) == 0 and omit_custom_fields):
            custom_fields_json = []
            for field in self.custom_fields:
                custom_fields_json.append(field.to_json())
            ret_user["custom_fields"] = custom_fields_json

        try:
            if self.has_bridge_id():
                ret_user["id"] = self.bridge_id
        except AttributeError:
            pass

        try:
            if self.first_name and len(self.first_name) > 0:
                ret_user["first_name"] = self.first_name
        except AttributeError:
            pass

        try:
            if self.last_name and len(self.last_name) > 0:
                ret_user["last_name"] = self.last_name
        except AttributeError:
            pass

        return ret_user

    def to_json_post(self):
        # for POST (add new user)
        return {"users": [self.json_data()]}

    def to_json_patch(self):
        # for PATCH, PUT (update)
        return {"user": self.json_data(omit_custom_fields=True)}

    def __str__(self):
        json_data = self.json_data()
        try:
            if self.sortable_name:
                json_data["sortable_name"] = self.sortable_name
        except AttributeError:
            pass
        try:
            if self.updated_at:
                json_data["updated_at"] = self.updated_at
        except AttributeError:
            pass
        try:
            if self.logged_in_at:
                json_data["logged_in_at"] = self.logged_in_at
        except AttributeError:
            pass
        try:
            json_data["completed_courses_count"] =\
                self.completed_courses_count
        except AttributeError:
            pass
        return json.dumps(json_data, default=str)

    def __init__(self, *args, **kwargs):
        super(BridgeUser, self).__init__(*args, **kwargs)
        self.custom_fields = []
        self.roles = []

    class Meta:
        db_table = "restclients_bridge_user"


class BridgeUserRole(models.Model):
    role_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(BridgeUserRole, self).__init__(*args, **kwargs)
        # self.permissions = []   # unknown 2016/11

    def to_json(self):
        return {
            "id": self.role_id,
            "name": self.name,
            # "permissions": self.permissions
            }

    def __str__(self):
        return json.dumps(self.to_json())

    class Meta:
        db_table = "restclients_bridge_user_role"
