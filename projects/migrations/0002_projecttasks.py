# Generated by Django 3.1.7 on 2022-05-26 05:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(default=0, null=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('IN-ACTIVE', 'IN-ACTIVE')], default='ACTIVE', max_length=30)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projecttasks_created_by', to=settings.AUTH_USER_MODEL)),
                ('project_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projecttasks_project_id', to='projects.projects')),
                ('tasks', models.ManyToManyField(blank=True, related_name='projecttasks_tasks', to='tasks.Tasks')),
            ],
            options={
                'verbose_name_plural': 'Project Tasks',
            },
        ),
    ]
