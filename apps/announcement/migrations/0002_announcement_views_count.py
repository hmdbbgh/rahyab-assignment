# Generated by Django 4.1.4 on 2023-07-23 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='views_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Announcement views count'),
        ),
    ]