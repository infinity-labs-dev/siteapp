from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from projects.models.projects import Projects
from tasks.models.tasks import Tasks
from sites.models.sites import Sites

class SiteTaskMapper(models.Model):
    CURRENT_STATUS = (
        ('PENDING', 'PENDING'),
        ('IN PROGRESS', 'IN PROGRESS'),
        ('COMPLETE', 'COMPLETE'),
    )
    
    projects = models.ForeignKey(Projects, blank=True, null=True, related_name="sitetaskmapper_projects", on_delete=models.CASCADE)
    sites = models.ForeignKey(Sites, blank=True, null=True, related_name="sitetaskmapper_sites", on_delete=models.CASCADE)
    tasks = models.ForeignKey(Tasks, blank=True, null=True, related_name='sitetaskmapper_tasks', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30,
        choices=CURRENT_STATUS,
        default='PENDING',
        blank=True, 
        null=True
    )
    file = models.FileField(upload_to=None, max_length=254, blank=True, null=True)
    created_by = models.ForeignKey(User, default=1, blank=True, related_name="sitetaskmapper_created_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)    
    class Meta:
        verbose_name_plural = "Site Tasks Mapper"