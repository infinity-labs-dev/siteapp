import csv, io, sys
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q
from resource_tracking.models import FaultManagement

class FaultImages(models.Model):
    fault = models.ForeignKey(FaultManagement, on_delete=models.CASCADE)
    image_name = models.ImageField(upload_to="fault_images", null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, )
    modified_at = models.DateTimeField(auto_now=True,  blank=True, null=True, )
    created_by = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name='FaultSiteImages_created_by')
    modified_by = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name='FaultSiteImages_modified_by')
   