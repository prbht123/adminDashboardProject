# Generated by Django 2.2 on 2022-07-15 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminDashboardApp', '0003_adminuserroles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuserroles',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_user_role', to=settings.AUTH_USER_MODEL),
        ),
    ]
