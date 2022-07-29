from django import forms
from django.contrib.auth.models import User
from adminDashboardApp.models import EmployeeProfile, AdminUserRoles, Department, ZoomMeetings, ZoomMeetingsUsers


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class EmployeePersonalDetailForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput)
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput)

    class Meta:
        model = EmployeeProfile
        fields = ['first_name', 'last_name', 'age',
                  'address', 'contact_number', 'gender']


class AdminUserRolesForm(forms.ModelForm):
    class Meta:
        model = AdminUserRoles
        fields = ['user', 'roles']


class AttendanceDetailForm(forms.Form):
    file_name = forms.FileField(
        label="Upload the files", widget=forms.FileInput)
    emp_id = forms.CharField(
        label="Enter Employee's ID", widget=forms.TextInput)
    fields = ['file_name', 'emp_id']


class EmployeeDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['company', 'department_name', 'employee']


class ZoomMeetingsForm(forms.ModelForm):
    class Meta:
        model = ZoomMeetings
        fields = ['meeting_topic', 'meeting_date',
                  'meeting_time', 'meeting_duration']


class ZoomMeetingsUsersForm(forms.ModelForm):
    class Meta:
        model = ZoomMeetingsUsers
        fields = ['zoom_meeting', 'users', 'users_staff']


class ZoomMeetingsSendMailForm(forms.ModelForm):
    class Meta:
        model = ZoomMeetingsUsers
        fields = ['message']
