# Generated by Django 4.1.4 on 2023-07-24 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='announcements_count',
        ),
    ]
