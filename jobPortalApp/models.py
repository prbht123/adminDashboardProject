from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.utils.crypto import get_random_string
from adminDashboardApp.models import Company
# Create your models here.

CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Internship', 'Internship'),
    ('Remote', 'Remote'),
)


class JobUsersProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='job_profile')
    id = models.AutoField(primary_key=True)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    slug = models.SlugField(max_length=500)
    higer_secondary_year = models.IntegerField(blank=True)
    secondary_year = models.IntegerField(blank=True)
    grad_year = models.IntegerField(blank=True)
    post_grad_year = models.IntegerField(blank=True)
    looking_for = models.CharField(
        max_length=30, choices=CHOICES, default='Full Time', null=True)

    def save(self, *args, **kwargs):
        the_slug = get_random_string(10, '012345675765676789')
        self.slug = slugify(self.user.username + the_slug)
        super(JobUsersProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=500)
    skill = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, related_name='skills', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        the_slug = get_random_string(10, '012345675765676789')
        self.slug = slugify(self.user.username + the_slug)
        super(Skill, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class AddressDetails(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=500)
    street = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    pincode = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        the_slug = get_random_string(10, '012345675765676789')
        self.slug = slugify(self.street + the_slug)
        super(AddressDetails, self).save(*args, **kwargs)

    def __str__(self):
        return self.city


class JobDetails(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=500)
    company = models.ForeignKey(
        Company, related_name='Company_job', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, null=True)
    job_description = models.CharField(max_length=600, null=True)
    experiance = models.CharField(max_length=255, null=True)
    salary = models.CharField(max_length=255, null=True)
    address = models.ForeignKey(AddressDetails, on_delete=models.CASCADE)
    hiring_members = models.BigIntegerField()
    industry_type = models.CharField(max_length=255, null=True)
    employement_type = models.CharField(
        max_length=30, choices=CHOICES, default='Full Time', null=True)
    qualification = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        the_slug = get_random_string(10, '012345675765676789')
        self.slug = slugify(self.job_title + the_slug)
        super(JobDetails, self).save(*args, **kwargs)

    def __str__(self):
        return self.job_title


class AppliedJobs(models.Model):
    CHOICE = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )
    job = models.ForeignKey(
        JobDetails, related_name='applied_job', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='applied_user', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=30, choices=CHOICE, default='Pending', null=True)

    def __str__(self):
        return self.job.job_title
