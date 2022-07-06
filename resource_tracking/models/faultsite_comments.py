import csv, io, sys
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q
from resource_tracking.models import FaultManagement
from django.utils import timezone

class FaultComments(models.Model):

    fault = models.ForeignKey(FaultManagement, on_delete=models.CASCADE)    
    comments = models.TextField(default="", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True,  blank=True, null=True, )
    created_by = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name='FaultComments_created_by')
    modified_by = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name='FaultComments_modified_by')
    def __str__(self):
        return str(self.fault)
    class Meta:
        verbose_name_plural = 'Fault Comments'