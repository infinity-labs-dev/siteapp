from resource_tracking.models.fault_management import FaultManagement
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from resource_tracking.models.faultsite_images import FaultImages

from sites.models.sitetasksummary import SiteTaskSummary


class FaultManagementSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = FaultManagement
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group        
        fields = ('id', 'name')      

class SiteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultImages        
        fields = '__all__'    

class SiteTaskSummarySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = SiteTaskSummary
        fields = '__all__'
