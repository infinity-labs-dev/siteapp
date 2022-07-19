from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from sites.models.sites import Sites
from sites.models.sitetaskmapper import SiteTaskMapper

class SiteTaskSummary(models.Model):
    TASK_STATUS = (
        ('STAND BY', 'STAND BY'),
        ('START TRACKING', 'START TRACKING'),
        ('END TRACKING', 'END TRACKING'),
    )
    sites = models.ForeignKey(Sites, blank=True, null=True, related_name="SiteTaskSummary_sites", on_delete=models.CASCADE)
    task_mapper_id = models.ForeignKey(SiteTaskMapper, blank=True, null=True, related_name='SiteTaskSummary_task_mapper_id', on_delete=models.CASCADE)
    site_engineer = models.ForeignKey(User, default=1, blank=True, related_name="SiteTaskSummary_site_engineer", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30,
        choices=TASK_STATUS,
        default='STAND BY',
        blank=True, 
        null=True
    )
    created_by = models.ForeignKey(User, default=1, blank=True, related_name="SiteTaskSummary_created_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name_plural = "Site Task Summary"