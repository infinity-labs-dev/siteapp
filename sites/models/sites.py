from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from projects.models.projects import Projects

class Sites(models.Model):
    CURRENT_STATUS = (
        ('PENDING', 'PENDING'),
        ('IN PROGRESS', 'IN PROGRESS'),
        ('COMPLETE', 'COMPLETE'),
    )
    
    SITE_TYPE = (
        ('HUB', 'HUB'),
        ('SPOKE', 'SPOKE'),
    )
    
    SITE_TYPE = (
        ('HUB', 'HUB'),
        ('SPOKE', 'SPOKE'),
    )

    VERIFICATION_STATUS = (
        ('PENDING', 'PENDING'),
        ('IN PROGRESS', 'IN PROGRESS'),
        ('WAITING-FOR-APPROVAL', 'WAITING-FOR-APPROVAL'),
        ('COMPLETE', 'COMPLETE'),
    )
    
    project_id = models.ForeignKey(Projects, blank=True, null=True, related_name="sites_project_id", on_delete=models.CASCADE)
    site_name = models.CharField(max_length=255, default="")
    serial_number = models.CharField(max_length=255, default="")
    spoc_name = models.CharField(max_length=255, default="")
    spoc_contact = models.CharField(max_length=255, default="")
    location = models.CharField(max_length=255, default="")
    site_details = models.TextField(default="")
    address = models.TextField(default="")
    latitude = models.CharField(max_length=20, default="")
    longitude = models.CharField(max_length=20, default="")
    date = models.DateTimeField(default=timezone.now)    
    scheduled_date = models.DateTimeField(default=timezone.now)
    completed_date = models.DateTimeField(default=timezone.now)
    site_engineer = models.ManyToManyField(User, blank=True,related_name='Site_site_engineer')
    primary_link = models.CharField(max_length=255, default="")
    primary_link_testing = models.CharField(max_length=255, default="")
    secondary_link = models.CharField(max_length=255, default="")
    secondary_link_testing = models.CharField(max_length=255, default="")
    site_status = models.CharField(
        max_length=30,
        choices=CURRENT_STATUS,
        default='PENDING',
    )
    site_type = models.CharField(
        max_length=30,
        choices=SITE_TYPE,
        default='PENDING',
    )
    verification_status = models.CharField(
        max_length=30,
        choices=VERIFICATION_STATUS,
        default='PENDING',
    )
    accpeted_by_id=models.ForeignKey(User, blank=True, null=True, related_name="sites_accpeted_by_id", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Site Master"

    def __str__(self):
        return self.site_name

    @staticmethod
    def get_all_categories():
        return Sites.objects.all()