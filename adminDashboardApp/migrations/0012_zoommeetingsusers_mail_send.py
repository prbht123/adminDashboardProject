# Generated by Django 4.0.6 on 2022-07-28 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminDashboardApp', '0011_zoommeetingsusers_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='zoommeetingsusers',
            name='mail_send',
            field=models.BooleanField(default=False),
        ),
    ]