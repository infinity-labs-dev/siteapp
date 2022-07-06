import csv, io, sys
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q
from sites.models.sites import Sites

class FaultAssignment(models.Model):
    site_data = models.FileField(upload_to='media')

    created_at = models.DateTimeField(auto_now_add=True, )
    created_by = models.ForeignKey(
                    User,
                    on_delete=models.CASCADE,
                    related_name='FaultAssignment_created_by')
    modified_at = models.DateTimeField(auto_now=True,  blank=True, null=True, )
    modified_by = models.ForeignKey(
                    User,
                    on_delete=models.CASCADE,
                    related_name='FaultAssignment_modified_by')
    def __str__(self):
        return str(self.id)
    class Meta:

        verbose_name_plural = 'Fault Assignment'
