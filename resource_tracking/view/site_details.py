from django.http.response import JsonResponse


from django.db.models import Q
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from resource_tracking.models.fault_management import FaultManagement
import json

class GetSiteDetails(APIView):

    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        faultId=request.get('fault_id')
        FaultMaster=FaultManagement.objects.filter(id=faultId)
        print(FaultMaster)
        content ={'id':1,}
        return Response(content)