from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Projects(models.Model):
        
    project_id = models.CharField(max_length=50, default="")
    project_name = models.CharField(max_length=50, default="")
    project_details = models.TextField(default="")
    created_by = models.ForeignKey(User, blank=True, default=1, null=True, related_name="projects_created_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Project Master"

    def __str__(self):
        return self.project_id