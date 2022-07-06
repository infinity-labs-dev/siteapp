import csv, io, sys
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q
from django.utils import tree
from sites.models.sites import Sites
from resource_tracking.models.fault_management import FaultManagement
from django.contrib.auth.models import Group


class SiteTracking(models.Model):

    STATUS = [
        ('Start Tracking', 'Start Tracking'),
        ('Start Tracking', 'End Tracking'),
        
    ]

    ticket= models.ForeignKey(FaultManagement, on_delete=models.CASCADE, related_name='SiteTracking_user')
    latitude = models.CharField(max_length=20, default="")
    longitude = models.CharField(max_length=20, default="")
    address=models.TextField(default="", null=True, blank=True)
    distance = models.FloatField(default=0.0)
    status = models.CharField(max_length=50, default="", null=True, blank=True)
    total_time = models.FloatField(default=0.0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, )
    created_by = models.ForeignKey(
                    User,
                    on_delete=models.CASCADE,
                    related_name='SiteTracking_created_by')
    modified_at = models.DateTimeField(auto_now=True,  blank=True, null=True, )
    modified_by = models.ForeignKey(
                    User,
                    on_delete=models.CASCADE,
                    related_name='SiteTracking_modified_by')
    status_comment=models.TextField(default="", null=True, blank=True)

    Group.add_to_class('hierarchy_level', models.IntegerField(default=0,null=True,blank=True))

    def __str__(self):
        return str(self.ticket)
    class Meta:
        verbose_name_plural = 'Site Tracking'

