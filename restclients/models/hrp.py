from django.db import models
from restclients.models.base import RestClientsModel


class AppointeePerson(models.Model):
    # employment status codes
    STATUS_ACTIVE = "A"

    # On Off Campus codes
    ON_SEATTLE_CAMPUS = "1"
    JOINT_CENTER_FOR_GRADUATE_STUDY = "3"
    FRIDAY_HARBOR_LABORATORIES = "4"
    REGIONAL_MEDICAL_LIBRARY = "6"
    COMPOSITE_LOCATIONS = "7"
    HARBORVIEW_MEDICAL_CENTER = "A"
    VETERANS_HOSPITAL = "B"
    US_PUBLIC_HEALTH_SERVICE_HOSPITAL = "C"
    CHILDRENS_ORTHOPEDIC_MEDICAL_CENTER = "D"
    FIRCREST_LABORATORY = "E"
    PROVIDENCE_MEDICAL_CENTER = "F"
    APPLIED_PHYSIC_LABORATORY = "G"
    PRIMATE_CENTER_SPECIAL_LOCATION = "H"
    ON_SEATTLE_CAMPUS_OTHER = "N"
    TACOMA_CAMPUS = "T"
    BOTHELL_WOODINVILLE_CAMPUS = "W"
    OFF_CAMPUS_ASSIGNMENT = "Y"
    OFF_CAMPUS_OTHER = "Z"

    # home_dept_org_code 1st digit"
    UW_SEATTLE = "2"
    MEDICAL_HEALTH_SCIENCES = "3"
    ADMIN_MANAGEMENT = "4"
    UW_BOTHELL = "5"
    UW_TACOMA = "6"

    regid = models.CharField(max_length=32,
                             db_index=True,
                             unique=True)
    eid = models.CharField(max_length=9,
                           db_index=True,
                           unique=True)
    status = models.CharField(max_length=2)
    status_desc = models.CharField(max_length=16)
    home_dept_budget_number = models.CharField(max_length=16)
    home_dept_budget_name = models.CharField(max_length=128,
                                             null=True)
    home_dept_org_code = models.CharField(max_length=16)
    home_dept_org_name = models.CharField(max_length=128,
                                          null=True)
    campus_code = models.CharField(max_length=2)
    campus_code_desc = models.CharField(max_length=32)

    def is_active_emp_status(self):
        return self.status == AppointeePerson.STATUS_ACTIVE

    def json_data(self):
        return {
            'regid': self.regid,
            'eid': self.eid,
            'status': self.status,
            'is_active': self.is_active_emp_status(),
            'status_desc': self.status_desc,
            'home_dept_budget_number': self.home_dept_budget_number,
            'home_dept_budget_name': self.home_dept_budget_name,
            'home_dept_org_code': self.home_dept_org_code,
            'home_dept_org_name': self.home_dept_org_name,
            'campus_code': self.campus_code,
            'campus_code_desc': self.campus_code_desc
            }

    def __str__(self):
        return "{%s: %s, %s: %s, %s: %s, %s: %s, %s: %s, %s: %s, %s: %s, %s: %s, %s: %s, %s: %s, %s: %s}" % (
            'regid', self.regid,
            'eid', self.eid,
            'status', self.status,
            'is_active', self.is_active_emp_status(),
            'status_desc', self.status_desc,
            'home_dept_budget_number', self.home_dept_budget_number,
            'home_dept_budget_name', self.home_dept_budget_name,
            'home_dept_org_code', self.home_dept_org_code,
            'home_dept_org_name', self.home_dept_org_name,
            'campus_code', self.campus_code,
            'campus_code_desc', self.campus_code_desc)
