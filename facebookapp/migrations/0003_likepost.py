# Generated by Django 2.2 on 2023-01-04 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebookapp', '0002_delete_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
    ]
