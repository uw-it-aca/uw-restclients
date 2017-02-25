from restclients_core import models
from restclients.models.base import RestClientsModel


class Appointment(models.Model):
    CURRENT_STATE = 'CURRENT'
    ACTIVE_STATUS = 'A'

    app_number = models.PositiveSmallIntegerField()
    app_state = models.CharField(max_length=16)
    dept_budget_name = models.CharField(max_length=96)
    dept_budget_number = models.CharField(max_length=16)
    job_class_code = models.CharField(max_length=16)
    job_class_title = models.CharField(max_length=96)
    org_code = models.CharField(max_length=16)
    org_name = models.CharField(max_length=96)
    paid_app_code = models.CharField(max_length=8)
    status = models.CharField(max_length=8)
    status_desc = models.CharField(max_length=16)

    def __cmp__(self, other):
        if other is not None:
            return self.app_number.__cmp__(other.app_number)

    def __lt__(self, other):
        return self.app_number < other.app_number

    def is_active_app_status(self):
        return self.status == Appointment.ACTIVE_STATUS

    def is_current_app_state(self):
        return self.app_state.upper() == Appointment.CURRENT_STATE

    def json_data(self):
        return {
            'app_number': self.app_number,
            'app_state': self.app_state,
            'dept_budget_name': self.dept_budget_name,
            'dept_budget_number': self.dept_budget_number,
            'job_class_code': self.job_class_code,
            'job_class_title': self.job_class_title,
            'org_code': self.org_code,
            'org_name': self.org_name,
            'paid_app_code': self.paid_app_code,
            'status': self.status,
            'status_desc': self.status_desc,
            }

    def __str__(self):
        return ("{%s: %s, %s: %s, %s: %s, %s: %s," +
                " %s: %s, %s: %s, %s: %s, %s: %s,"
                " %s: %s, %s: %s, %s: %s}") % (
            'app_number', self.app_number,
            'app_state', self.app_state,
            'dept_budget_name', self.dept_budget_name,
            'dept_budget_number', self.dept_budget_number,
            'job_class_code', self.job_class_code,
            'job_class_title', self.job_class_title,
            'org_code', self.org_code,
            'org_name', self.org_name,
            'paid_app_code', self.paid_app_code,
            'status', self.status,
            'status_desc', self.status_desc
            )

    class Meta:
        db_table = 'restclients_hrp_appointment'


class Appointee(models.Model):
    # employment status codes
    STATUS_ACTIVE = "A"
    STATUS_RETIREE = "R"
    STATUS_SEPARATED = "S"

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

    netid = models.SlugField(max_length=32,
                             db_index=True,
                             unique=True)
    regid = models.CharField(max_length=32,
                             db_index=True,
                             unique=True)
    employee_id = models.CharField(max_length=9,
                                   db_index=True,
                                   unique=True)
    status = models.CharField(max_length=2)
    status_desc = models.CharField(max_length=16)
    home_dept_budget_number = models.CharField(max_length=16)
    home_dept_budget_name = models.CharField(max_length=96,
                                             null=True)
    home_dept_org_code = models.CharField(max_length=16)
    home_dept_org_name = models.CharField(max_length=96,
                                          null=True)
    onoff_campus_code = models.CharField(max_length=2)
    onoff_campus_code_desc = models.CharField(max_length=32)

    def __init__(self):
        self.appointments = []

    def is_active_emp_status(self):
        return self.status == Appointee.STATUS_ACTIVE

    def json_data(self):
        apps = []
        for app in self.appointments:
            apps.append(app.json_data())

        return {
            "netid": self.netid,
            'regid': self.regid,
            'employee_id': self.employee_id,
            'status': self.status,
            'is_active': self.is_active_emp_status(),
            'status_desc': self.status_desc,
            'home_dept_budget_number': self.home_dept_budget_number,
            'home_dept_budget_name': self.home_dept_budget_name,
            'home_dept_org_code': self.home_dept_org_code,
            'home_dept_org_name': self.home_dept_org_name,
            'onoff_campus_code': self.onoff_campus_code,
            'onoff_campus_code_desc': self.onoff_campus_code_desc,
            'appointments': apps
            }

    def __str__(self):
        return ("{%s: %s, %s: %s, %s: %s, %s: %s," +
                " %s: %s, %s: %s, %s: %s, %s: %s,"
                " %s: %s, %s: %s, %s: %s, %s: %s, %s: [%s]}") % (
            "netid", self.netid,
            'regid', self.regid,
            'employee_id', self.employee_id,
            'status', self.status,
            'is_active', self.is_active_emp_status(),
            'status_desc', self.status_desc,
            'home_dept_budget_number', self.home_dept_budget_number,
            'home_dept_budget_name', self.home_dept_budget_name,
            'home_dept_org_code', self.home_dept_org_code,
            'home_dept_org_name', self.home_dept_org_name,
            'onoff_campus_code', self.onoff_campus_code,
            'onoff_campus_code_desc', self.onoff_campus_code_desc,
            'appointments', ','.join(map(str, self.appointments))
            )

    class Meta:
        db_table = 'restclients_hrp_appointee'
