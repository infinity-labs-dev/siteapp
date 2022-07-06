import io, sys
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.http import response
from resource_tracking.models.fault_management import FaultManagement


class PushNotificationLog(models.Model):
    fault = models.ForeignKey(
                    FaultManagement, 
                    on_delete=models.CASCADE, 
                    related_name='PushNotificationLog_fault')
    notification_response = models.TextField(default="", null=True, blank=True)
    user = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name='PushNotificationLog_user')
    created_at = models.DateTimeField(auto_now_add=True, )  
    created_by = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name='PushNotificationLog_created_by')
    modified_at = models.DateTimeField(auto_now=True,  blank=True, null=True, )
    modified_by = models.ForeignKey(
                    User, 
                    on_delete=models.CASCADE, 
                    related_name='PushNotificationLog_modified_by')
    def __str__(self):
        return str(self.fault)
    class Meta:
        verbose_name_plural = 'Push Notification Log'
