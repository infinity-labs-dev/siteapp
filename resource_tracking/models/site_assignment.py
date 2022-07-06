import csv, io, sys
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q
from sites.models.sites import Sites


class SiteAssignement(models.Model):
    user= models.ManyToManyField(User,related_name='SiteAssignement_user',verbose_name="siteassign_user")
    site= models.ForeignKey(Sites, on_delete=models.CASCADE, related_name='SiteAssignement_site',verbose_name="Site")
    created_at = models.DateTimeField(auto_now_add=True, )
    created_by = models.ForeignKey(
                    User,
                    on_delete=models.CASCADE,
                    related_name='SiteAssignement_created_by')
    modified_at = models.DateTimeField(auto_now=True,  blank=True, null=True, )
    modified_by = models.ForeignKey(
                    User,
                    on_delete=models.CASCADE,
                    related_name='SiteAssignement_modified_by')

    def __str__(self):
        return str(self.site)
    class Meta:
        verbose_name_plural = 'Site Assignment'
