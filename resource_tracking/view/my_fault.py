from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField
from django.http.response import JsonResponse
from django.db import models
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from resource_tracking.models.fault_management import FaultManagement
from sites.models.sites import Sites
from resource_tracking.models.site_tracking import SiteTracking
from resource_tracking.models import FaultImages
from resource_tracking.models.faultsite_comments import FaultComments
from resource_tracking.models.site_assignment import SiteAssignement
from django.core import serializers
from django.http import JsonResponse
from resource_tracking.serializers import FaultManagementSerializer
from resource_tracking.serializers import SiteImageSerializer
import datetime
from datetime import timedelta
import socket
import json
from push_notifications.models import APNSDevice, GCMDevice
import requests
from django.conf import settings

# from django.contrib.gis.geos.point import Point
from django.contrib.gis.geos import GEOSGeometry
from geopy.geocoders import GoogleV3

from django.db import connection
from django.utils.timezone import utc
from resource_tracking.models.push_notification_log import PushNotificationLog
from resource_tracking.utils import saveSiteTracking
from projects.models.projecttasks import ProjectTasks
from sites.models.sitetaskmapper import SiteTaskMapper

# view fault site list
class MyFault(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        # print("user =", request.user)
        # for g in request.user.groups.all():
        #     l.append(g.id)

        faultLists=Sites.objects.filter(site_engineer=request.user)
        print(faultLists.query)
        faultArray=[]
        if faultLists:
            for faultList in faultLists:
                assignedDate = str(datetime.datetime.strftime(faultList.created_at, "%d-%m-%Y %I:%M%p"))
                accpeted_by=0
                if faultList.accpeted_by_id:
                    accpeted_by=faultList.accpeted_by_id
                innserarray={}
                innserarray.update({"site_id": faultList.id, "project_id": faultList.project_id_id, "site_name":faultList.site_name, 'site_details':faultList.site_details, "spoc_name": faultList.spoc_name, "spoc_contact": faultList.spoc_contact, "scheduled_date": faultList.scheduled_date, 'address': faultList.address, 'verification_status':faultList.verification_status, "latitude":faultList.latitude, "longitude":faultList.longitude, 'accpeted_by': accpeted_by, 'assigned_at': assignedDate})
                faultArray.append(innserarray)

            message = ""
            return Response({"data":faultArray,"sucess":True, "message":message})
        else:
            faultArray = []
            message = "No Result Found."
            return Response({"data":faultArray,"sucess":False, "message":message})


# view fault site details by id
class MyFaultView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FaultManagementSerializer, SiteImageSerializer,
    def get(self, request):

        try:
            #  static vars
            httpString=""
            if request.is_secure():
                httpString="https://"
            else:
                httpString="http://"
            fault_id = self.request.query_params.get('fault_id')
            if fault_id is not None and fault_id != '' :

                faultLists=Sites.objects.filter(id=fault_id, site_engineer=request.user)
                # import pdb;pdb.set_trace()
                faultArray=[]
                if faultLists:
                    for faultList in faultLists:
                        tasksarray=[]
                        
                        assignedDate = str(datetime.datetime.strftime(faultList.created_at, "%d-%m-%Y %I:%M%p"))
                        
                        accpeted_by=0
                        if faultList.accpeted_by_id and faultList.accpeted_by_id is not None:
                            accpeted_by=faultList.accpeted_by_id
                        
                        # get comment data
                        comments=getFaultComments(fault_id)
                        
                        # tasks
                        tasks = SiteTaskMapper.objects.raw('SELECT * FROM sites_sitetaskmapper WHERE sites_id ='+ str(faultList.id))
                        # print(tasks)
                        for t in tasks:
                            tasksArray={}
                            tasksArray.update({"row_id": t.id, "sites_id": t.sites_id, "site_name": t.sites.site_name, "projects_id": t.projects_id, "project_id_name": t.projects.project_id, "project_name": t.projects.project_name, "tasks_id": t.tasks_id, "task_name": t.tasks.task_name, "status": t.status, "file": str(t.file), "created_at": t.created_at})
                            # print("tasksArray", tasksArray)
                            tasksarray.append(tasksArray)
                        
                        
                        innserarray={}
                        innserarray.update({"site_id": faultList.id, "project_id": faultList.project_id_id, "site_name":faultList.site_name, 'site_details':faultList.site_details, "spoc_name": faultList.spoc_name, "spoc_contact": faultList.spoc_contact, "scheduled_date": faultList.scheduled_date, 'verification_status':faultList.verification_status, "latitude":faultList.latitude, "longitude":faultList.longitude, 'comments':comments, 'accpeted_by': accpeted_by, 'assigned_at': assignedDate, "tasks": tasksarray})
    
                        faultArray.append(innserarray)
                        
                    faultImages = FaultImages.objects.filter(fault_id=fault_id)
                                        
                    imageArray=["https://siteappsoftware.pythonanywhere.com/media/"]

                    # import pdb;pdb.set_trace()
                    message = ""
                    return Response({"data":faultArray, "image_url":imageArray, "sucess":True, "message":message})
                else:
                    faultArray = []                    
                    imageArray=[httpString+request.META['SERVER_NAME']+"/media/"]
                    message = "No Result Found."
                    return Response({"data":faultArray, "image_url":imageArray, "sucess":False, "message":message})
            else:
                faultArray = []
                imageArray=["https://siteappsoftware.pythonanywhere.com/media/"]
                message = "fault_id missing"
                return Response({"data":faultArray, "image_url":imageArray,"sucess":False, "message":message})

        except Exception as e:
            print("error ***", e)
            faultArray = []
            imageArray=["https://siteappsoftware.pythonanywhere.com/media/"]
            # message = "Something went wrong"
            message = str(e)

            return Response({"data":faultArray, "images":imageArray, "sucess":False, "message":message})


def getFaultComments(fault_id):

        Faultcomment= FaultComments.objects.filter(fault_id=fault_id).order_by("-created_at")
        commentString=""
        for comments in Faultcomment:
            datetimenow=datetime.datetime.strftime(comments.created_at, "%d-%m-%Y %I:%M%p")
            comm = "<div><p> <b style='float: left;'>"+ comments.created_by.first_name +"</b> <span style='float: right;'>"+ datetimenow +"</span><br /> <span>"+ comments.comments +"</span></p></div>"

            commentString=commentString+comm

        return commentString


# update my fault status by id
class UpdateMyFaultStatus(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FaultManagementSerializer
    def post(self, request):

        data = json.loads(request.body)

        # data=request.data
        fault_id = data['fault_id']
        user_id = data['user_id']
        status = data['status']
        latitude = data['latitude']
        longitude = data['longitude']

        comment = ''
        if "comment" in data:
            comment=data['comment']

        admin_remark = ''
        if "admin_remark" in data:
            admin_remark=data['admin_remark']

        address = ''
        if "address" in data:
            address=data['address']

        status_comment=''
        if "status_comment" in data:
            status_comment=data['status_comment']
            
        status=''
        if "status" in data:
            status=data['status']    

        message="Status Updation Inprocess"
        faultArray=[]
        result=FaultManagement.objects.filter(id=fault_id).update(status=status)
        if(result > 0):

            first_name = request.user.first_name
            # import pdb;pdb.set_trace()

            # datetimenow = str(datetime.datetime.now())
            datetimenow = datetime.datetime.now()
            datetimenow=datetime.datetime.strftime(datetimenow, "%d-%m-%Y %I:%M%p")

            distancekm = 0
            total_time=0

            faultData=FaultManagement.objects.get(id=fault_id)
            if comment is not None and comment != '':
                faultComment= FaultComments()
                faultComment.fault=faultData
                faultComment.comments=comment
                faultComment.created_by=request.user
                faultComment.modified_by=request.user
                faultComment.save()

            if admin_remark is not None and admin_remark != '':

                faultData.admin_remark = "<b>"+ datetimenow +  "</b>: " + admin_remark + " <br />" + faultData.admin_remark

                faultData.admin_remark = admin_remark
                faultData.save()          

            # accepted by updation in fault
            if status == "Accepted":
                # print(status)
                faultData.accpeted_by = request.user
                faultData.save()

            checkLastTrack=SiteTracking.objects.filter(ticket_id=fault_id,created_by=request.user).exclude(status="Fault Assigned").last()
            if checkLastTrack:

                # return Response('here in already')
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
                sitetrack.ticket_id = fault_id
                sitetrack.latitude = latitude
                sitetrack.longitude = longitude
                sitetrack.created_by_id = user_id
                sitetrack.modified_by_id = user_id
                sitetrack.distance = round(distancekm,2)
                sitetrack.status = status
                sitetrack.address=address
                sitetrack.status_comment=status_comment
                sitetrack.total_time=total_time
                sitetrack.save()

            else:

                # insert tracking data into 'SiteTracking model'
                sitetrack = SiteTracking()
                sitetrack.ticket_id = fault_id
                sitetrack.latitude = latitude
                sitetrack.longitude = longitude
                sitetrack.created_by_id = user_id
                sitetrack.modified_by_id = user_id
                sitetrack.distance = distancekm
                sitetrack.status = status
                sitetrack.address=address
                sitetrack.status_comment=status_comment
                sitetrack.total_time=total_time
                sitetrack.save()

            message = "Updated"
            responseStatus = True
            faultLists=FaultManagement.objects.filter(id=fault_id)
            faultArray=[]
            for faultList in faultLists:
                assignedDate = str(datetime.datetime.strftime(faultList.created_at, "%d-%m-%Y %I:%M%p"))
                accpeted_by=0
                if faultList.accpeted_by_id and faultList.accpeted_by_id is not None:
                    accpeted_by=faultList.accpeted_by_id
                innserarray={}
                comments=getFaultComments(fault_id)
                innserarray.update({"site_id": faultList.site.id, "site_name":faultList.site.site_name, 'fault_description':faultList.fault_description, 'status':faultList.status, 'fault_id':faultList.id, "latitude":faultList.site.latitude, "longitude":faultList.site.longitude, 'comments':comments, 'admin_remark':faultList.admin_remark, 'accpeted_by': accpeted_by, 'assigned_at': assignedDate})
                faultArray.append(innserarray)
                # send push notification
                message=""
                if status =="Accepted":
                    message=faultList.site.site_name+' is accepted'
                elif status =="Rejected":
                    message=faultList.site.site_name+' is Rejected'
                if message!="":
                    sendUserList=SiteAssignement.objects.get(site=faultList.site)
                    alluser=sendUserList.user.all()
                    for user in alluser:
                        if user!=request.user:
                            print("here")
                            pushResponse = send_push_notification(user,message)
                            if pushResponse:
                                    pushObject = PushNotificationLog()
                                    pushObject.user = request.user
                                    pushObject.fault = faultList
                                    pushObject.notification_response = pushResponse
                                    pushObject.created_by = request.user
                                    pushObject.modified_by = request.user
                                    pushObject.save()
        else:
            message = "Failed"
            responseStatus = False

        return Response({"data":faultArray, "message":message, "sucess":responseStatus})


def send_push_notification(user,message):
        device = GCMDevice.objects.get(user=user)
        if device:
            deviceToken=device.registration_id
            # print("Token",deviceToken)
            serverToken =settings.PUSH_NOTIFICATIONS_SETTINGS['FCM_API_KEY']
            # print("Server",serverToken)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=' + serverToken,
            }
            body = {
                'data': {
                    'title': 'Fault Assignment',
                    'body': message
                },
                'to':
                    deviceToken,
                'priority': 'high',
                # 'data': dataPayLoad,
            }
            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
            # check what is the response
            # print(response)
            
            return response


# Update Resolved status with multiple image upload
class ResolvedMyFaultStatus(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FaultManagementSerializer
    def post(self, request):

        # data = json.loads(request.body)

        data=request.data

        fault_id = data['fault_id']
        user_id = data['user_id']
        status = data['status']
        latitude = data['latitude']
        longitude = data['longitude']

        address=data['address']
        faultArray=[]
        comment = ''
        if "comment" in data:
            comment=data['comment']

        fault_type = ''
        if "fault_type" in data:
            fault_type=data['fault_type']

        message="Status Updation Inprocess"
        result=FaultManagement.objects.filter(id=fault_id).update(status=status)

        if fault_type is not None and fault_type != '':
                 result2=FaultManagement.objects.filter(id=fault_id).update(fault_type=fault_type)

        if(result > 0):

            first_name = request.user.first_name

            # datetimenow = str(datetime.datetime.now())
            datetimenow = datetime.datetime.now()
            datetimenow=datetime.datetime.strftime(datetimenow, "%d-%m-%Y %I:%M%p")

            filedata = dict((request.FILES).lists()).get('Image', None)
            # import pdb;pdb.set_trace()
            faultData=FaultManagement.objects.get(id=fault_id)
            if filedata:

                for photo in filedata:
                    photo_data = {}
                    photo_data["fault"] = fault_id
                    photo_data["image_name"] = photo
                    photo_data["created_by"] = user_id
                    photo_data["modified_by"] = user_id
                    photo_serializer = SiteImageSerializer(data=photo_data)
                    photo_serializer.is_valid(raise_exception=True)
                    photo_serializer.save()
            distancekm = 0
            total_time=0
            if comment is not None and comment != '':
                faultComment= FaultComments()
                faultComment.fault=faultData
                faultComment.comments=comment
                faultComment.created_by=request.user
                faultComment.modified_by=request.user
                faultComment.save()

            checkLastTrack=SiteTracking.objects.filter(ticket_id=fault_id,created_by=request.user).last()
            if checkLastTrack:

                # return Response('here in already')
                datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
                date1 = str(datetime.datetime.now())
                date2 = str(checkLastTrack.created_at.replace(tzinfo=None))
                diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)

                # print("Difference:", diff)
                # print("Days:", diff.days)
                # print("Microseconds:", diff.microseconds)
                # print("Seconds:", diff.seconds)


                # listmunites=str(diff).split(":")
                # total_time=int(listmunites[0])*60+int(listmunites[1])
                # if diff:

                #     listmunites=str(diff).split(":")
                #     total_time=int(listmunites[0])*60+int(listmunites[1])
                # else:
                total_time = 0


                # print("minutes:", total_time)
                lat = checkLastTrack.latitude
                long = checkLastTrack.longitude
                # import pdb;pdb.set_trace()
                pnt = GEOSGeometry('SRID=4326;POINT('+str(long)+' '+str(lat)+')')
                pnt2 = GEOSGeometry('SRID=4326;POINT('+str(longitude)+' '+str(latitude)+')')
                distancekm = pnt.distance(pnt2) * 100
                # return Response({"kmdist":distancekm})


                # insert tracking data into 'SiteTracking model'
                sitetrack = SiteTracking()
                sitetrack.ticket_id = fault_id
                sitetrack.latitude = latitude
                sitetrack.longitude = longitude
                sitetrack.created_by_id = user_id
                sitetrack.modified_by_id = user_id
                sitetrack.distance = round(distancekm,2)
                sitetrack.status = status
                sitetrack.address=address
                sitetrack.total_time=total_time
                sitetrack.save()

                # make End Work entry
                if(status == "Resolved"):
                    sitetrack1 = SiteTracking()
                    sitetrack1.ticket_id = fault_id
                    sitetrack1.latitude = latitude
                    sitetrack1.longitude = longitude
                    sitetrack1.created_by_id = user_id
                    sitetrack1.modified_by_id = user_id
                    sitetrack1.distance =0
                    sitetrack1.status = "End Work"
                    sitetrack1.address=address
                    sitetrack1.total_time=0
                    sitetrack1.save()

            else:

                # return Response('here in not already')
                # insert tracking data into 'SiteTracking model'
                sitetrack = SiteTracking()
                sitetrack.ticket_id = fault_id
                sitetrack.latitude = latitude
                sitetrack.longitude = longitude
                sitetrack.created_by_id = user_id
                sitetrack.modified_by_id = user_id
                sitetrack.distance = distancekm
                sitetrack.status = status
                sitetrack.address=address
                sitetrack.total_time=total_time
                sitetrack.save()

                # make End Work entry
                if(status == "Resolved"):
                    sitetrack1 = SiteTracking()
                    sitetrack1.ticket_id = fault_id
                    sitetrack1.latitude = latitude
                    sitetrack1.longitude = longitude
                    sitetrack1.created_by_id = user_id
                    sitetrack1.modified_by_id = user_id
                    sitetrack1.distance = distancekm
                    sitetrack1.status = "End Work"
                    sitetrack1.address=address
                    sitetrack1.total_time=total_time
                    sitetrack1.save()


            message = "Updated"
            responseStatus = True
            faultLists=FaultManagement.objects.filter(id=fault_id)
            faultArray=[]
            for faultList in faultLists:
                assignedDate = str(datetime.datetime.strftime(faultList.created_at, "%d-%m-%Y %I:%M%p"))
                accpeted_by=0
                if faultList.accpeted_by_id and faultList.accpeted_by_id is not None:
                    accpeted_by=faultList.accpeted_by_id

                innserarray={}
                comments=getFaultComments(fault_id)
                innserarray.update({"site_name":faultList.site.site_name,'fault_description':faultList.fault_description,'status':faultList.status,'fault_id':faultList.id,"latitude":faultList.site.latitude,"longitude":faultList.site.longitude,'comments':comments,'admin_remark':faultList.admin_remark,'fault_type':faultList.fault_type, 'accpeted_by': accpeted_by, 'assigned_at': assignedDate})
                faultArray.append(innserarray)
                message=""
                if status =="Resolved":
                    message=faultList.site.site_name+' is resolved'

                if message!="":
                    sendUserList=SiteAssignement.objects.get(site=faultList.site)
                    alluser=sendUserList.user.all()
                    for user in alluser:
                        if user!=request.user:
                            print("here")
                            pushResponse = send_push_notification(user,message)
                            if pushResponse:
                                    pushObject = PushNotificationLog()
                                    pushObject.user = request.user
                                    pushObject.fault = faultList
                                    pushObject.notification_response = pushResponse
                                    pushObject.created_by = request.user
                                    pushObject.modified_by = request.user
                                    pushObject.save()

        else:
            message = "Failed to Resolved please try again"
            responseStatus = False

        return Response({"data":faultArray, "message":message, "sucess":responseStatus})


class UpdateTaskDetails(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            # static vars
            httpString=""
            if request.is_secure():
                httpString="https://"
            else:
                httpString="http://"
                
            imageArray=["https://siteappsoftware.pythonanywhere.com/media/"]          
            
            faultArray=[]
                
            data=request.data
            row_id = data['row_id']
            user_id = data['user_id']
            status = data['status']
            file = request.data['file']
            # print("file", file)

            result = SiteTaskMapper.objects.get(id=row_id)
            result.status = status
            result.file=file
            result.save()
            
            updatedResult = SiteTaskMapper.objects.filter(id=row_id)
            if updatedResult:
                for t in updatedResult:
                    innserarray={}
                    innserarray.update({"row_id": t.id, "sites_id": t.sites_id, "site_name": t.sites.site_name, "projects_id": t.projects_id, "project_id_name": t.projects.project_id, "project_name": t.projects.project_name, "tasks_id": t.tasks_id, "task_name": t.tasks.task_name, "status": t.status, "file": str(t.file), "created_at": t.created_at})
        
                    faultArray.append(innserarray)
            
            message = "Task details updated successfully"            
            return Response({"data":faultArray, "image_url":imageArray, "sucess":True, "message":message})
            
        except Exception as e:
            print("error ***", e)
            faultArray = []            
            # imageArray=[httpString+socket.gethostname()+"/media/"]
            imageArray=["https://siteappsoftware.pythonanywhere.com/media/"]
            # message = "Something went wrong"
            message = str(e)

            return Response({"data":faultArray, "images":imageArray, "sucess":False, "message":message})
