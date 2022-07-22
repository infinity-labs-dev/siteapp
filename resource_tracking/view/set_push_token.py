from pdb import set_trace
from django.db.models.fields import NullBooleanField
from django.http.response import JsonResponse
from django.db import models
from django.db import connection


from django.db.models import Q
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from resource_tracking.models.fault_management import FaultManagement

from django.core import serializers
from django.http import JsonResponse
from resource_tracking.serializers import FaultManagementSerializer
from resource_tracking.serializers import SiteTaskSummarySerializer
from push_notifications.models import APNSDevice, GCMDevice

from django.db.models import Q
from django.conf import settings


import json
import requests


# Get Fault List By Status
class SetPushToken(APIView):
    permission_classes = (IsAuthenticated,)
    #serializer_class = FaultManagementSerializer
    serializer_class = SiteTaskSummarySerializer
    def get(self, request):
        
        device = GCMDevice.objects.get(user=request.user)
        #result=device.send_message(message={"title" : "Game Request", "body" : "Bob wants to play poker"})
        #return Response({"data":result})

        if device:
            deviceToken=device.registration_id
            #print(deviceToken)
            #serverToken = 'BEDH8OBSVsAlX5LUEne2xUsp587YP5moRMM7etPOZC3rNzSYzZHH-X9SSimiwPeWlFKS4ksPGMa4K1ZkQLNSuRA'
            serverToken = 'BDfucXWTxD8XpvomGW0jD0HRZGlwjYKwJkb-q3WsZnyoHxhX7_pefXXFuPmK_S5R2LTsX-Kmi4f_8b60tRNmlBs'
            #deviceToken = 'fjPY93E_Sg2iidOFMFPcTz:APA91bGWvMc9AyNBiiSq_Mn52ne7dCL95zEUo_YXqGbPGJAoRh3cjVuDOyNKLyN5dvEsMDCW9oFXlh5-NJ23OTxy1vj1tIJ0tPdCBe1eWnYXvS-Z22XQsa8F-Jsvz3LhmiEV-iOWhp8b'
        headers = {
               'Content-Type': 'application/json',
               'Authorization': 'key =' +serverToken,
            }

        body = {
                'data': {'title': 'Fault Assigned !',
                                    'body': 'Pradeep Site assigned to you, please check'
                                    },
                'to':
                    deviceToken,
                'priority': 'high',
                #   'data': dataPayLoad,
                }
        response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
        #print(response)
        if request.is_secure():
            httpString="https://"
        else:
            httpString="http://"
        return Response({"data":response,"sucess":True,"message":"","path":headers})


    def post(self, request):

        sucess=False
        message=""
        try:
            data = json.loads(request.body)
            user_id = data['user_id']
            registration_id = data['registration_id']
            username= data['username']
            # import pdb;pdb.set_trace()
            if registration_id and user_id:

                getDeviceData = GCMDevice.objects.filter(user_id=user_id)
                if getDeviceData:
                    fcm_device = GCMDevice.objects.filter(user_id=user_id).update(registration_id=registration_id)
                else:
                   fcm_device = GCMDevice.objects.create(registration_id=registration_id, cloud_message_type="FCM", user=request.user,name=username)
                sucess=True
                message="message true"

            else:
                sucess=False
                message="registration id missing or user_id"

        except Exception as e:
                sucess=False
                print(e)
                message=str(e)

        return Response({"data":"","success":sucess,"message":message})

