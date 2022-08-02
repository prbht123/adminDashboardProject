# Generated by Django 4.0.6 on 2022-08-01 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminDashboardApp', '0015_remove_skill_user_delete_jobusersprofile_and_more'),
        ('jobPortalApp', '0002_jobusersprofile_id_alter_jobusersprofile_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('slug', models.SlugField(max_length=500)),
                ('street', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=255, null=True)),
                ('state', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=255, null=True)),
                ('pincode', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('slug', models.SlugField(max_length=500)),
                ('job_title', models.CharField(max_length=255, null=True)),
                ('job_description', models.CharField(max_length=600, null=True)),
                ('experiance', models.CharField(max_length=255, null=True)),
                ('salary', models.CharField(max_length=255, null=True)),
                ('hiring_members', models.BigIntegerField()),
                ('industry_type', models.CharField(max_length=255, null=True)),
                ('employement_type', models.CharField(choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time'), ('Internship', 'Internship'), ('Remote', 'Remote')], default='Full Time', max_length=30, null=True)),
                ('qualification', models.CharField(max_length=255, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobPortalApp.addressdetails')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Company_job', to='adminDashboardApp.company')),
            ],
        ),
    ]