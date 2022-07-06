from django.db import models
from django.conf import settings
import os

class  Conversation(models.Model):
    participant_ids=models.TextField(null = True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, auto_now=False,)
    created_by = models.ForeignKey(
                    settings.AUTH_USER_MODEL, 
                    on_delete=models.CASCADE, 
                    default=1,
                    related_name='Conversation_created_by')
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True,)
    modified_by = models.ForeignKey(
                    settings.AUTH_USER_MODEL, 
                    default=1,
                    on_delete=models.CASCADE, 
                    related_name='Conversation_modified_by')
    
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Conversations"
        