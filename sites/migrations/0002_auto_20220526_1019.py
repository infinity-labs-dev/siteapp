# Generated by Django 3.1.7 on 2022-05-26 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttasks',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='projecttasks_tasks', to='tasks.Tasks'),
        ),
        migrations.DeleteModel(
            name='Tasks',
        ),
    ]
