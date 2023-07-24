# Generated by Django 4.1.4 on 2023-07-23 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='اضافه شده در')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='اصلاح شده در')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('accepted', models.BooleanField(default=False, verbose_name='Accepted')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcments', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
