from pdb import set_trace
from django.db.models.fields import NullBooleanField
from django.http.response import JsonResponse
from django.db import models
from django.db import connection


from django.db.models import Q
import datetime
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from resource_tracking.models.fault_management import FaultManagement

from django.core import serializers
from django.http import JsonResponse
from resource_tracking.serializers import FaultManagementSerializer

from django.db.models import Q

import json


# Get Fault List By Status
class GetFaultListByStatus(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FaultManagementSerializer
    def get(self, request):
        # data = json.loads(request.body)
        data = request.GET
        # print(data)

        user_id = data['user_id']
        status = data['status']
        # import pdb; set_trace()

        faultArray = []
        message = ''

        # l = []
        # for g in request.user.groups.all():
        #     l.append(g.id)

        faultLists=FaultManagement.objects.filter(status=status, user=request.user)
        # faultLists=FaultManagement.objects.filter(status=status, role__in=l).query
        # print(faultLists)
        # import pdb; set_trace()
        if faultLists:

            for faultList in faultLists:
                assignedDate = str(datetime.datetime.strftime(faultList.created_at, "%d-%m-%Y %I:%M%p"))

                innserarray={}
                innserarray.update({"site_name":faultList.site.site_name,'fault_description':faultList.fault_description,'status':faultList.status,'fault_id':faultList.id,"type":faultList.site.type,"nominal_name":faultList.site.nominal_id,"latitude":faultList.site.latitude,"longitude":faultList.site.longitude,'site_type':faultList.site.site_type_master.site_name,'admin_remark':faultList.admin_remark,'fault_type':faultList.fault_type, 'accpeted_by': faultList.accpeted_by_id, 'assigned_at': assignedDate})
                faultArray.append(innserarray)

            message = ""
            return Response({"data":faultArray,"sucess":True,"message":message})
        else:
            faultArray = []
            message = "No Result Found."
            return Response({"data":faultArray,"sucess":False,"message":message})

