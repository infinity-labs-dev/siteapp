from django.db import models
from django.conf import settings
import os
from .conversation import Conversation

class  Message(models.Model):
    text=models.TextField(null = True, default='')
    conversation=models.ForeignKey(
                    Conversation, 
                    on_delete=models.CASCADE, 
                    null = True,
                    default='',
                    related_name='Message_conversation')
    sender_id=models.ForeignKey(
                    settings.AUTH_USER_MODEL, 
                    on_delete=models.CASCADE, 
                    default=1,
                    related_name='Message_sender_id')
    receivers_ids=models.TextField(default='', null = True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, auto_now=False,)
    created_by = models.ForeignKey(
                    settings.AUTH_USER_MODEL, 
                    on_delete=models.CASCADE, 
                    default=1,
                    related_name='Message_created_by')
    modified_at = models.DateTimeField(auto_now=True,  blank=True, null=True, )
    modified_by = models.ForeignKey(
                    settings.AUTH_USER_MODEL, 
                    default=1,
                    on_delete=models.CASCADE, 
                    related_name='Message_modified_by')
    
    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "Messages"
        