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
from push_notifications.models import APNSDevice, GCMDevice

from django.db.models import Q
from django.conf import settings


import json
import requests


# Get Fault List By Status
class SetPushToken(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FaultManagementSerializer
    def get(self, request):

        device = GCMDevice.objects.get(user=request.user)
        # result=device.send_message(message={"title" : "Game Request", "body" : "Bob wants to play poker"})
        # return Response({"data":result})

        if device:
            deviceToken=device.registration_id
            print(deviceToken)
        serverToken = 'AAAAYPp4Yno:APA91bGnqQXODPLw07e41hgFsqtoJZmulIi49S-w-f1Aa5oGg_7e4xeTXnPv4hdy8FjMCaaGvT1r5psDD1Ch9WU9V46C8fKggrUAvweNtKSdU7k5OYXelVTpeLNYRRu9aSVj0zxkJ2Mz'
        # deviceToken = 'cxMg7GDBSGCOL5TX1gzw_6:APA91bHKJ8OQJ8zWhfV6koiaKCbE44D0X853PMSLonpjWaq8pw2fESc8e1vl_oqRJphjmwPWnBHXnxLGimys2nI_EELJ9dG0ISAqLqn2WDd1Ly1r90l6Cn8h0Esf_BfEyN_T6b6sbkXU'

        headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=' + serverToken,
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
        if request.is_secure():
            httpString="https://"
        else:
            httpString="http://"
        return Response({"data":response,"sucess":True,"message":"","path":httpString+request.META['SERVER_NAME']+"/media/fault_images/IMG_20210810_145756_57.jpg"})


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
                message=""

            else:
                sucess=False
                message="registration id missing or user_id"

        except Exception as e:
                sucess=False
                print(e)
                message=str(e)

        return Response({"data":"","success":sucess,"message":message})

