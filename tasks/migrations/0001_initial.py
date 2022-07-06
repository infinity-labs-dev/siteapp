# Generated by Django 3.1.7 on 2022-05-26 04:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(default='', max_length=50)),
                ('description', models.TextField(default='')),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('IN PROGRESS', 'IN PROGRESS'), ('COMPLETE', 'COMPLETE')], default='PENDING', max_length=30)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Task Master',
            },
        ),
    ]
