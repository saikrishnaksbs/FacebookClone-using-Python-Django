# Generated by Django 2.2 on 2023-01-06 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebookapp', '0006_auto_20230106_0519'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]