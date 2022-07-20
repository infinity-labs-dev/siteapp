#from email.policy import default
#from re import T
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
    RESOURCE_FLAG = (
        ('YES', 'YES'),
        ('NO', 'NO'),
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
    sequence_no = models.IntegerField(blank=True, null=True)
    site_engineer = models.ForeignKey(User, default=1, blank=True, related_name="sitetaskmapper_site_engineer", on_delete=models.CASCADE)
    resource_flag = models.CharField(
        max_length=30,
        choices=RESOURCE_FLAG,
        default='NO',
        blank=True, 
        null=True
    )    
    class Meta:
        verbose_name_plural = "Site Tasks Mapper"