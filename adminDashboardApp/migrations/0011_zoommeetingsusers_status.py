# Generated by Django 4.0.6 on 2022-07-28 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminDashboardApp', '0010_alter_zoommeetings_meeting_zoom_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='zoommeetingsusers',
            name='status',
            field=models.CharField(choices=[('complete', 'Completed'), ('pending', 'Pending'), ('cancel', 'Canceled')], default='pending', max_length=250),
        ),
    ]