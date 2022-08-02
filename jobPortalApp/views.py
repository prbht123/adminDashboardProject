from multiprocessing import get_context
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, CreateView, ListView, DetailView, DeleteView
from django.contrib.auth.models import User
from .models import JobDetails, JobUsersProfile, Skill, AddressDetails, AppliedJobs
from .forms import JobUsersProfileForm, UserSkillForm, JobDetailsForm
from adminDashboardApp.models import Department
# Create your views here.


def homejob(request):
    pass


class jobUserProfileListView(ListView):
    """
        User can show the details of job profile.
    """
    model = JobUsersProfile
    #template_name = 'jobs/job_profile_job_list.html'
    template_name = 'jobs/job.html'
    context_object_name = "jobuserprofile"

    def get_queryset(self):
        # original qs
        qs = super().get_queryset()
        # filter by a variable captured from url, for example
        context = {}
        context['user_job_profile'] = qs.filter(
            user__username=self.request.user.username)
        if context['user_job_profile']:
            context['user_job_profile'] = context['user_job_profile'][0]

        context['skill'] = Skill.objects.filter(
            user__username=self.request.user.username)
        user_department = Department.objects.filter(
            employee__username=self.request.user.username, department_name='hr')
        if user_department:
            context['user_department'] = user_department[0].employee.username
        else:
            context['user_department'] = None
        print(context['user_department'])
        return context


class jobUserProfileCreateView(CreateView):
    """
        User can add the profile for getting jobs.
    """
    form_class = JobUsersProfileForm
    template_name = 'jobs/create_user_profile_job.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        user = User.objects.get(id=self.request.user.id)
        data.user = user
        data.save()
        return redirect('jobs:user_skill_job_create')


class jobUserProfileUpdateView(UpdateView):
    """
        User can edit the profile for getting jobs.
    """
    model = JobUsersProfile
    form_class = JobUsersProfileForm
    success_url = '/jobs/userjobsprofile/'
    template_name = 'jobs/update_user_job_profile.html'

    def get_form_kwargs(self):
        kwargs = super(jobUserProfileUpdateView, self).get_form_kwargs()
        kwargs.update()
        return kwargs


class jobUserProfileDeleteView(DeleteView):
    template_name = 'jobs/delete_user_job_profile.html'
    model = JobUsersProfile
    success_url = '/jobs/userjobsprofile/'


class jobUserSkillCreateView(CreateView):
    """
        User can add the Skills for getting jobs.
    """
    form_class = UserSkillForm
    template_name = 'jobs/user_skill_job_create.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        user_name = User.objects.get(id=self.request.user.id)
        data.user = user_name
        data.save()
        return redirect('jobs:user_job_profile')


class jobUserSkillDeleteView(DeleteView):
    template_name = 'jobs/delete_user_skill.html'
    model = Skill
    success_url = '/jobs/userjobsprofile/'


class jobCreateView(CreateView):
    """
        Hrs can add the Job for company.
    """
    form_class = JobDetailsForm
    template_name = 'jobs/create_jobs.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        street = self.request.POST['street']
        city = self.request.POST['city']
        state = self.request.POST['state']
        country = self.request.POST['country']
        pin_code = self.request.POST['pin_code']
        address = AddressDetails.objects.create(
            street=street, city=city, state=state, country=country, pincode=pin_code)
        data.address = address
        data.save()
        return redirect('jobs:user_job_profile')


class jobListView(ListView):
    """
        Display the all jobs for company.
    """
    model = JobDetails
    template_name = 'jobs/list_jobs.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        # original qs
        qs = super().get_queryset()
        # filter by a variable captured from url, for example
        context = {}
        context['job_list'] = qs
        user_department = Department.objects.filter(
            employee__username=self.request.user.username, department_name='hr')
        if user_department:
            context['user_department'] = user_department[0].employee.username
        else:
            context['user_department'] = None
        return context


class jobUpdateView(UpdateView):
    """
        Hrs can update the Job for company.
    """
    model = JobDetails
    form_class = JobDetailsForm
    success_url = '/jobs/joblist/'
    template_name = 'jobs/hrUsers/update_job.html'

    def get_form_kwargs(self):
        address = AddressDetails.objects.get(id=self.object.address.id)
        kwargs = super(jobUpdateView, self).get_form_kwargs()
        street = self.request.POST.get('street')
        city = self.request.POST.get('city')
        state = self.request.POST.get('state')
        country = self.request.POST.get('country')
        pin_code = self.request.POST.get('pin_code')
        if street:
            address.street = street
        if city:
            address.city = city
        if state:
            address.state = state
        if country:
            address.country = country
        if pin_code:
            address.pincode = pin_code
        address.save()
        kwargs.update()
        return kwargs


class jobDeleteView(DeleteView):
    """
        Hrs can delete the Job for company.
    """
    template_name = 'jobs/hrUsers/delete_job.html'
    model = JobDetails
    success_url = '/jobs/joblist/'


def jobAppliedCreateView(request, slug):
    user = User.objects.get(username=request.user.username)
    job = JobDetails.objects.get(slug=slug)
    data = AppliedJobs.objects.filter(user=user, job=job)

    if not data:
        data = AppliedJobs.objects.create(user=user, job=job)

    return redirect('jobs:job_list')


class jobAppliedUsersListView(ListView):
    model = AppliedJobs
    template_name = 'jobs/users/applied_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = AppliedJobs.objects.filter(
            job__slug=self.kwargs['slug'])
        print(context['users'])
        return context


class jobAppliedByUserListView(ListView):
    model = AppliedJobs
    template_name = 'jobs/users/applied_jobs_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = AppliedJobs.objects.filter(
            user__username=self.request.user.username)
        print(context['users'])
        return context
