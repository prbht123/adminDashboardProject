from django.contrib import admin
from adminDashboardApp.models import EmployeeProfile, Company, Department, Attendance, AdminUserRoles, ZoomMeetings, ZoomMeetingsUsers


admin.site.register(EmployeeProfile)
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Attendance)
admin.site.register(AdminUserRoles)
admin.site.register(ZoomMeetings)
admin.site.register(ZoomMeetingsUsers)
