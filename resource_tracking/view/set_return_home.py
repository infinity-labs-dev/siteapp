from pdb import set_trace

import requests
from resource_tracking.models.site_tracking import SiteTracking
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

from django.db.models import Q

import json
from django.contrib.gis.geos import GEOSGeometry
from geopy.geocoders import GoogleV3
from push_notifications.models import APNSDevice, GCMDevice
from django.utils.timezone import utc
from resource_tracking.models.push_notification_log import PushNotificationLog
import datetime
from datetime import timedelta,date

# Get Fault List By Status
class SetReturnHome(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FaultManagementSerializer
    def post(self, request):
        # data = json.loads(request.body)        
        data = json.loads(request.body)
        # print(data)
        user_id = data['user_id']
        latitude = data['latitude']
        longitude = data['longitude']
        address = data['address']
        status= data['status']
        faultArray = []
        message = ''  
        distancekm=0
        checkLastTrack=SiteTracking.objects.filter(created_by=request.user).order_by("-created_at").last()
        if checkLastTrack is not None:
            datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
            date1 = str(datetime.datetime.now())
            date2 = str(checkLastTrack.created_at.replace(tzinfo=None))
            diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
            # print("Difference:", diff)
            # print("Days:", diff.days)
            # print("Microseconds:", diff.microseconds)
            # print("Seconds:", diff.seconds)
            sec_value = diff.seconds % (24 * 3600)
            hour_value = sec_value // 3600
            sec_value %= 3600
            min = sec_value // 60
            # print("hourvalue",hour_value)
            # print("min value",min)
            # listmunites=str(diff).split(":")
            total_time=int(hour_value)*60+int(min)

            # print("minutes:", total_time)
            lat = checkLastTrack.latitude
            long = checkLastTrack.longitude

            if status != "Accepted":
                pnt = GEOSGeometry('SRID=4326;POINT('+str(long)+' '+str(lat)+')')
                pnt2 = GEOSGeometry('SRID=4326;POINT('+str(longitude)+' '+str(latitude)+')')
                distancekm = pnt.distance(pnt2) * 100
                # return Response({"kmdist":distancekm})
            # insert tracking data into 'SiteTracking model'
            sitetrack = SiteTracking()
            sitetrack.ticket = checkLastTrack.ticket
            sitetrack.latitude = latitude
            sitetrack.longitude = longitude
            sitetrack.created_by_id = user_id
            sitetrack.modified_by_id = user_id
            sitetrack.distance = round(distancekm,2)
            sitetrack.status = status
            sitetrack.address=address
            sitetrack.total_time=total_time
            sitetrack.save()
            print("Last Ticket id",checkLastTrack)
            faultLists=FaultManagement.objects.filter(user=request.user).exclude(status__in=["Approved","Pending"]).exclude(id=checkLastTrack.ticket_id)
            if faultLists:
                for faultList in faultLists:
                    checkLastTrack=SiteTracking.objects.filter(ticket=faultList).filter(created_at__date=date.today()).last()
                    print("Looping Tiket Id",checkLastTrack)
                    if checkLastTrack is not None:
                        sitetrack = SiteTracking()
                        sitetrack.ticket = checkLastTrack.ticket
                        sitetrack.latitude = latitude
                        sitetrack.longitude = longitude
                        sitetrack.created_by_id = user_id
                        sitetrack.modified_by_id = user_id
                        sitetrack.distance = 0
                        sitetrack.status = status
                        sitetrack.address=address
                        sitetrack.total_time=0
                        sitetrack.save()     
                        
                message = ""
                return Response({"data":faultArray,"sucess":True,"message":message})
            else:
                faultArray = []
                message = "No Result Found."
                return Response({"data":faultArray,"sucess":False,"message":message})

        return Response({"data":faultArray,"sucess":False,"message":message})
