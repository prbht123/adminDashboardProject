from django import forms
from django.contrib.auth.models import User
from .models import JobUsersProfile, Skill, JobDetails, AddressDetails, AppliedJobs


class JobUsersProfileForm(forms.ModelForm):
    class Meta:
        model = JobUsersProfile
        fields = ['secondary_year', 'higer_secondary_year',
                  'grad_year', 'post_grad_year', 'looking_for', 'resume']


class UserSkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill']


class JobDetailsForm(forms.ModelForm):
    class Meta:
        model = JobDetails
        fields = ['company', 'job_title', 'job_description', 'experiance', 'salary',
                  'hiring_members', 'industry_type', 'employement_type', 'qualification']
