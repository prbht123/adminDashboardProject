from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from adminDashboardApp.forms import UserForm, EmployeePersonalDetailForm, \
    AdminUserRolesForm, AttendanceDetailForm, EmployeeDepartmentForm, ZoomMeetingsForm, ZoomMeetingsUsersForm, ZoomMeetingsSendMailForm
from adminDashboardApp.models import EmployeeProfile, AdminUserRoles, Company, Department, ZoomMeetings, ZoomMeetingsUsers
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView

from datetime import datetime
from django.template.loader import render_to_string
from django.http import HttpResponse
import weasyprint
from weasyprint import HTML, CSS
import os
import io
from django.views.generic.edit import FormView
from django.conf import settings
import jwt
import requests
import json
from time import time
from .utills import createMeeting
from django.core.mail import send_mail


def adminDashboard(request):
    return render(request, 'dashboard/dashboard.html')


def employeeDetailList(request):
    employees = EmployeeProfile.objects.filter(
        user__is_staff=False, user__is_active=True)
    return render(request, 'Employee/display_user.html', {'employees': employees,
                                                          'admin': False})


def adminDetailList(request):
    employees = EmployeeProfile.objects.filter(
        user__is_staff=True, user__is_active=True)
    return render(request, 'Employee/display_user.html', {'employees': employees,
                                                          'admin': True})


def employeeRegisterUser(request):
    """
        Employee can register new admin users.
    """

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the choosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return redirect('adminDashboardApp:employeePersonalDetail',
                            pk=new_user.id)

    else:
        user_form = UserForm()
        return render(request, 'Employee/create_user.html',
                      {'user_form': user_form})


def employeePersonalDetail(request, pk):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        age = request.POST['age']
        gender = request.POST['gender']
        contact = request.POST['contact_number']
        address = request.POST['address']

        user = User.objects.get(id=pk)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        employee = EmployeeProfile()
        employee.age = age
        employee.gender = gender
        employee.user = user
        employee.contact_number = contact
        employee.address = address
        employee.save()
        return redirect('adminDashboardApp:dashboard')
    else:
        personal_form = EmployeePersonalDetailForm()
        return render(request, 'Employee/personal_detail.html',
                      {'personal_form': personal_form})


class createRoleAdmin(CreateView):
    """
        Admin user can add the roles to particular admin users.
    """
    form_class = AdminUserRolesForm
    template_name = 'roles/create_role_admin_user.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        user = self.request.POST['user']
        user = User.objects.get(id=user)
        data.user = user
        data.save()
        return redirect('adminDashboardApp:createRole')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = AdminUserRoles.objects.all()
        return context


class roleUpdateView(UpdateView):
    """
        Admin users can update the roles of other admin users.
    """
    model = AdminUserRoles
    form_class = AdminUserRolesForm
    template_name = 'roles/edit_role_admin_user.html'
    success_url = '/createRole/'

    def get_form_kwargs(self):
        kwargs = super(roleUpdateView, self).get_form_kwargs()
        kwargs.update()
        return kwargs


class deleteAdminUserRoles(DeleteView):
    """
        Admin users can delete the roles of admin users.
    """
    model = AdminUserRoles
    template_name = 'roles/delete_role_admin_user.html'
    success_url = '/createRole/'


def convertNormalUserToAdmin(request, pk):
    """
        Admin users can make admin user from normal user.
    """
    if request.user.is_staff == True:
        user = User.objects.get(id=pk)
        user.is_staff = True
        user.save()
        return redirect('adminDjango:employee_list')


def convertAdminToNormal(request, pk):
    """
        Admin users can make admin user from normal user.
    """
    if request.user.is_staff == True:
        user = User.objects.get(id=pk)
        user.is_staff = False
        user.save()
        return redirect('adminDjango:admin_list')


def deactivatedUserByAdmin(request, pk, nm):
    """
        Admin users can make admin user from normal user.
    """
    if request.user.is_staff == True:
        user = User.objects.get(id=pk)
        if nm == "deactivate":
            user.is_staff = False
            user.is_active = False
        user.save()
        return redirect('adminDjango:admin_list')


def deactivatedUsers(request):
    employees = EmployeeProfile.objects.filter(user__is_active=False)
    return render(request, 'Employee/display_user.html', {'employees': employees,
                                                          'admin': True})


def activatedUsers(request, pk):
    """
        Admin users can make admin user from normal user.
    """
    if request.user.is_staff == True:
        user = User.objects.get(id=pk)
        user.is_staff = False
        user.is_active = True
        user.save()
        return redirect('adminDjango:deactivatedUsers')


class deleteDeactivatedUser(DeleteView):
    """
        Admin users can delete the roles of admin users.
    """
    model = User
    template_name = 'Employee/delete_user.html'
    success_url = '/deactivatedUsers/'


def attendance(request):
    if request.method == 'POST':

        id = request.POST['id']
        try:
            file_name = request.FILES['datafile']
            file = file_name.readlines()
        except:
            return render(request, 'attendanceRecord/attendance.html')

        result = []
        for item in file:
            data = {}
            all_data = (str(item)).replace("b\'", '')
            all_data = all_data.replace('\\t', ' ')
            all_data = all_data.replace('\\r', '')
            all_data = all_data.replace('\\n', '')
            all_data = (str(all_data)).split(' ')
            lst = []
            for i in all_data:
                if i != "":
                    lst.append(i)

            all_data = lst
            all_data[2] = datetime.strptime(all_data[2], '%H:%M:%S')

            value = 0
            for item in result:
                if all_data[0] == item['id'] and all_data[1] == item['date']:
                    if all_data[2]:
                        item['checkout'] = all_data[2]
                        if 'checkin' in item:
                            item['duration'] = item['checkout']-item['checkin']
                    value = 1
                    break
            if value == 0:
                data['id'] = all_data[0]
                if (all_data[2].time()).strftime("%p") == "PM":
                    data['checkout'] = all_data[2]
                else:
                    data['checkin'] = all_data[2]
                data['date'] = all_data[1]
                result.append(data)
        if id:
            result_id = []
            for item in result:
                if item['id'] == id:
                    result_id.append(item)
            context = {
                'result': result_id
            }
        else:
            context = {
                'result': result
            }

        return render(request, 'attendanceRecord/attendance.html', context)
    return render(request, 'attendanceRecord/attendance.html')


def joinLetter(request):
    return render(request, 'joiningLetter/join.html')


def convertPdf(request):
    if request.method == "POST":
        this_folder = os.path.dirname(os.path.abspath(__file__))
        print(this_folder)
        print("0000000000")
        context = {
            'emp_name': request.POST['emp_name'],
            'date': request.POST['date'],
            'position': request.POST['position'],
            'location': request.POST['location'],
            'pre_company': request.POST['pre_company'],
            'guardian': request.POST['guardian'],
            'image_path':  'file://' + os.path.join(this_folder, 'static', 'images', 'webkrone.png')
        }
        print(context['image_path'])
        print("11111111111")
        html = render_to_string('joiningLetter/pdf_change.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline:filename= "{}.pdf"'.format(
            "name")
        weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
            CSS(string='body { font-size: 13px }')])
        return response


def zoomMeeting(request):
    """
        Created Zoom meeting by Hr users only.
    """
    if request.method == "POST":
        topic = request.POST.get('topic', False)
        date = request.POST.get('startDate', False)
        time1 = request.POST.get('time', False)
        duration = request.POST.get('duration', False)
        date_time = date + "T" + time1 + ":00:00"
        createMeeting(topic, date_time, duration)
    user_department = Department.objects.filter(
        employee__username=request.user.username, department_name='hr')
    context = {}
    if user_department:
        context['user_department'] = user_department[0].employee.username
    else:
        context['user_department'] = None
    return render(request, 'Zoom/zoom.html', context)


class zoomMeetingCreateView(CreateView):
    """
        Hr user can create the zoom meetings for interviews.
    """

    form_class = ZoomMeetingsForm
    template_name = 'Zoom/zoom_meeting_create.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()
        topic = data.meeting_topic
        date_time = str(data.meeting_date) + 'T' + str(data.meeting_time)
        duration = data.meeting_duration
        zoom_meeting = createMeeting(topic, date_time, duration)
        data1 = ZoomMeetings.objects.get(id=data.id)
        data1.meeting_zoom_link = zoom_meeting['link']
        data1.meeting_zoom_password = zoom_meeting['password']
        data1.save()
        return redirect('adminDjango:zoom_meeting_user_create', pk=data.id)


class zoomMeetingUsersCreateView(CreateView):
    """
        Hr user can add the zoom meetings for interviews with users.
    """

    form_class = ZoomMeetingsUsersForm
    template_name = 'Zoom/zoom_meeting_user_create.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        zoom_meeting = self.request.POST['zoom_meeting']
        zoom_meeting = ZoomMeetings.objects.filter(id=zoom_meeting)[0]
        data.zoom_meeting = zoom_meeting
        data.save()
        return redirect('adminDjango:zoom_meeting')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zoom_meeting'] = ZoomMeetings.objects.filter(
            id=self.kwargs['pk'])[0]
        return context


class zoomMeetingListView(ListView):
    """
        Hr user can create the zoom meetings for interviews.
    """

    model = ZoomMeetings
    template_name = 'Zoom/zoom_meeting_list.html'
    queryset = ZoomMeetings.objects.all()


class zoomMeetingDetailView(DetailView):
    """
        User can see detail of the zoom meetings for interviews.
    """

    model = ZoomMeetings
    template_name = 'Zoom/zoom_meeting_user_deatil.html'

    def get_context_data(self, *args, **kwargs):
        context = super(zoomMeetingDetailView,
                        self).get_context_data(*args, **kwargs)
        context["zoom_meeting_users"] = ZoomMeetingsUsers.objects.filter(
            zoom_meeting__id=self.kwargs['pk'])
        if context['zoom_meeting_users']:
            context['zoom_meeting_users'] = context['zoom_meeting_users'][0]
        user_department = Department.objects.filter(
            employee__username=self.request.user.username, department_name='hr')
        if user_department:
            context['user_department'] = user_department[0].employee.username
        else:
            context['user_department'] = None

        if not context['zoom_meeting_users']:
            context['zoom_meeting'] = ZoomMeetings.objects.filter(
                id=self.kwargs['pk'])[0]

        return context


class zoomMeetingDeleteView(DeleteView):
    template_name = 'Zoom/zoom_meeting_delete.html'
    model = ZoomMeetings
    success_url = '/zoom_meeting_list/'


class zoomMeetingSendMailView(UpdateView):
    model = ZoomMeetingsUsers
    form_class = ZoomMeetingsSendMailForm
    success_url = '/zoom_meeting_list/'
    template_name = 'Zoom/zoom_meeting_send_mail.html'

    def get_form_kwargs(self):
        kwargs = super(zoomMeetingSendMailView, self).get_form_kwargs()
        kwargs['instance'].mail_send = True
        kwargs.update()

        users = kwargs['instance'].users + "," + kwargs['instance'].users_staff
        users = list(users.split(","))

        message = kwargs['instance'].zoom_meeting.meeting_zoom_link + \
            ' Paasword :  ' + \
            kwargs['instance'].zoom_meeting.meeting_zoom_password
        res = send_mail('zoom meeting link for interview', message,
                        'prabhat.webcrone@gmail.com', ['amit.webkrone@gmail.com', 'prabhat.webkrone@gmail.com', 'prabhat.webcrone@gmail.com'])
        return kwargs


class organisationView(ListView):
    template_name = 'Organisation/org_detail.html'
    model = Company
    queryset = Company.objects.all()


class departmentListView(ListView):
    """
        Admin user can See list of the departments to users and add,update and delete of department of a particular users.
    """
    model = Department
    template_name = 'departments/department.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_department = Department.objects.filter(
            employee__username=self.request.user.username, department_name='admin')
        if user_department:
            context['user_department'] = user_department[0].employee.username
        else:
            context['user_department'] = None

        context['hrs'] = Department.objects.filter(department_name='hr')
        context['backoffices'] = Department.objects.filter(
            department_name='backoffice')
        context['developers'] = Department.objects.filter(
            department_name='developer')
        context['designers'] = Department.objects.filter(
            department_name='designer')
        context['business_developments'] = Department.objects.filter(
            department_name='business_development')
        context['admins'] = Department.objects.filter(department_name='admin')
        return context


class departmentCreateView(CreateView):
    """
        Admin user can add the departments to users.
    """

    form_class = EmployeeDepartmentForm
    template_name = 'departments/user_department_create.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()
        return redirect('adminDjango:department')


class departmentUpdateView(UpdateView):
    """
        Admin users can update the department of users.
    """
    model = Department
    form_class = EmployeeDepartmentForm
    template_name = 'departments/user_department_update.html'
    success_url = '/department/'

    def get_form_kwargs(self):
        kwargs = super(departmentUpdateView, self).get_form_kwargs()
        kwargs.update()
        return kwargs


class departmentDeleteView(DeleteView):
    """
        Admin users can delete the department of users.
    """
    model = Department
    template_name = 'departments/user_department_delete.html'
    success_url = '/department/'
