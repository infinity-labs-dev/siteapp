import csv, io, sys
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q

class Attendance(models.Model):
   
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='Attendance_user')
    in_time = models.DateTimeField(auto_now_add=True,blank=True, null=True,verbose_name="In Time")
    out_time = models.DateTimeField(blank=True, null=True ,default=None,verbose_name="Out Time" )
    created_at = models.DateTimeField(auto_now_add=True, )
    
  
    class Meta:
        verbose_name_plural = 'Employee Attendance'

    