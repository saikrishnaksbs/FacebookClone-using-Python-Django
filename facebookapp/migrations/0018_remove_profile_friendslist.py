# Generated by Django 2.2 on 2023-01-08 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebookapp', '0017_profile_friendslist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='friendslist',
        ),
    ]
