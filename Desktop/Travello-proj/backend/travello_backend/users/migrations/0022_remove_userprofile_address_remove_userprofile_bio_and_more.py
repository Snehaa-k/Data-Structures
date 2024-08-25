# Generated by Django 5.0.7 on 2024-08-25 08:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_remove_userprofile_is_verified_lead'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='country_state',
        ),
        migrations.AddField(
            model_name='usermodels',
            name='address',
            field=models.TextField(max_length=345, null=True),
        ),
        migrations.AddField(
            model_name='usermodels',
            name='bio',
            field=models.CharField(max_length=234, null=True),
        ),
        migrations.AddField(
            model_name='usermodels',
            name='country_state',
            field=models.CharField(max_length=234, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]
