# Generated by Django 2.2 on 2023-01-08 06:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facebookapp', '0016_post_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friendslist',
            field=models.ManyToManyField(blank=True, related_name='friend', to=settings.AUTH_USER_MODEL),
        ),
    ]
