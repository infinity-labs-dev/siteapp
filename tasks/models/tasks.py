from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Tasks(models.Model):
    CURRENT_STATUS = (
        ('PENDING', 'PENDING'),
        ('IN PROGRESS', 'IN PROGRESS'),
        ('COMPLETE', 'COMPLETE'),
    )
    
    task_name = models.CharField(max_length=50, default="")
    description = models.TextField(default="")
    status = models.CharField(
        max_length=30,
        choices=CURRENT_STATUS,
        default='PENDING',
    )
    created_by = models.ForeignKey(User, blank=True, default=1, related_name="tasks_created_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Task Master"

    def __str__(self):
        return self.task_name