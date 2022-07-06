from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from projects.models.projects import Projects
from tasks.models.tasks import Tasks

class ProjectTasks(models.Model):
    CURRENT_STATUS = (
        ('ACTIVE', 'ACTIVE'),
        ('IN-ACTIVE', 'IN-ACTIVE'),
    )
    
    project_id = models.ForeignKey(Projects, blank=True, null=True, related_name="projecttasks_project_id", on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Tasks, blank=True,related_name='projecttasks_tasks')
    priority = models.IntegerField(default=0, null=True)
    status = models.CharField(
        max_length=30,
        choices=CURRENT_STATUS,
        default='ACTIVE',
    )
    created_by = models.ForeignKey(User, default=1, blank=True, related_name="projecttasks_created_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Project Tasks"

    # def __str__(self):
    #     return self.id