from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.utils.crypto import get_random_string


class EmployeeProfile(models.Model):
    GENDER = (
        ('Male', 'male'),
        ('Female', 'female')
    )
    age = models.IntegerField()
    gender = models.CharField(max_length=50, choices=GENDER, default='male')
    address = models.CharField(max_length=250)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    contact_number = models.BigIntegerField()

    def __str__(self):
        return self.user.first_name


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_apartment_num = models.CharField(max_length=255, null=True)
    company_street = models.CharField(max_length=255, null=True)
    company_city = models.CharField(max_length=255, null=True)
    company_state = models.CharField(max_length=255, null=True)
    company_country = models.CharField(max_length=255, null=True)
    company_contact_number = models.BigIntegerField()
    company_email_address = models.EmailField(max_length=255, null=True)

    def __str__(self):
        return self.company_name


class Department(models.Model):
    department_choices = (
        ('hr', 'Hr'),
        ('backoffice', 'Backoffice'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('business_development', 'Business_Development'),
        ('admin', 'Admin')

    )
    department_name = models.CharField(
        max_length=250, choices=department_choices, default='hr')
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='employee')
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='company')

    def __str__(self):
        return self.department_name


class Attendance(models.Model):
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='employeeAttendance')
    date_time = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.employee.first_name


class Role(models.Model):
    role_name = models.CharField(max_length=250)

    def __str__(self):
        return self.role_name


class EmployeeRole(models.Model):
    emp_role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='empRole')
    emp_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='empUser')

    def __str__(self):
        return self.employee.first_name


class AdminUserRoles(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=500)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="admin_user_role")
    roles = models.ForeignKey(
        Permission, on_delete=models.CASCADE, null=True, related_name='roles')

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        the_slug = get_random_string(10, '012345675765676789')
        self.slug = slugify(self.user.username + the_slug)
        super(AdminUserRoles, self).save(*args, **kwargs)


class ZoomMeetings(models.Model):
    meeting_topic = models.CharField(max_length=255)
    meeting_date = models.DateField()
    meeting_time = models.TimeField()
    meeting_duration = models.CharField(max_length=100)
    meeting_zoom_link = models.CharField(max_length=600, null=True)
    meeting_zoom_password = models.CharField(max_length=255, null=True)


class ZoomMeetingsUsers(models.Model):
    status_choice = (
        ('complete', 'Completed'),
        ('pending', 'Pending'),
        ('cancel', 'Canceled')
    )
    zoom_meeting = models.ForeignKey(ZoomMeetings, on_delete=models.CASCADE)
    users = models.CharField(max_length=555, null=True)
    users_staff = models.CharField(max_length=555, null=True)
    status = models.CharField(
        max_length=250, choices=status_choice, default='pending')
    mail_send = models.BooleanField(default=False)
    message = models.CharField(max_length=355, null=True)



