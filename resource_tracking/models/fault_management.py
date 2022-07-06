import csv, io, sys
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q
from sites.models.sites import Sites


class FaultManagement(models.Model):

    STATUS = [
        ('Task Assigned', 'Task Assigned'),
        ('Accepted', 'Accepted'),
        ('Start Tracking', 'Start Tracking'),
        ('End Tracking', 'End Tracking'),
        ('Closed', 'Closed'),
    ]

    FAULTTYPE=[
        ('Active Issue', 'Active Issue'),
        ('Passive Issue', 'Passive Issue'),
    ]
    
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='FaultManagement_user', verbose_name="user")
    site= models.ForeignKey(Sites, on_delete=models.CASCADE, related_name='FaultManagement_site',verbose_name="Site")    
    status = models.CharField( 
                    max_length=50,
                    choices=STATUS,
                    blank=True,
                    default="Task Assigned",)
    fault_description = models.TextField(default="", blank=True, null=True)
    admin_remark = models.TextField(default="", blank=True, null=True)
    # comments = models.TextField(default="", blank=True, null=True)
    resolved_date = models.DateTimeField(blank=True, null=True ,default=None,verbose_name="Resolved Date")
    created_at = models.DateTimeField(auto_now_add=True, )  
    created_by = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name='FaultManagement_created_by')
    modified_at = models.DateTimeField(auto_now=True,  blank=True, null=True, )
    modified_by = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name='FaultManagement_modified_by')

    approved_by = models.ForeignKey(
                    User, default=None,null=True,
                    on_delete=models.CASCADE, 
                    related_name='FaultManagement_approved_by')
    
    fault_type = models.CharField( 
                    max_length=50,
                    choices=FAULTTYPE,
                    blank=True,
                    default="Passive Issue",)
    accpeted_by = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    blank=True, null=True,
                    related_name='FaultManagement_accpeted_by')
                    
    
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural = 'Task Management'

    
