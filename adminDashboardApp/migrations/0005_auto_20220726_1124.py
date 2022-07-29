# Generated by Django 2.2 on 2022-07-26 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminDashboardApp', '0004_auto_20220715_0744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='company_address',
        ),
        migrations.RemoveField(
            model_name='company',
            name='company_email',
        ),
        migrations.AddField(
            model_name='company',
            name='company_apartment_num',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='company_city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='company_country',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='company_email_address',
            field=models.EmailField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='company_state',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='company_street',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='department',
            name='department_name',
            field=models.CharField(choices=[('hr', 'Hr'), ('backoffice', 'Backoffice'), ('developer', 'Developer'), ('designer', 'Designer'), ('business_development', 'Business_Development')], default='hr', max_length=250),
        ),
    ]
