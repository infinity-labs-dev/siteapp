from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import pdb
import json
import requests
from django.conf import settings
from chat.models import Conversation
from push_notifications.models import GCMDevice

# add user chat
class AddConversation(APIView):
    def post(self, request):
        try:
            data={}
            path = request.build_absolute_uri('/')
            other = [{"base_image_path":path}]
            
            inputdata=json.loads(request.body)
            
            message = "Conversation added successfully"
            return Response({"data": data, "sucess":True, "message":message, "other": other})    
        except Exception as e:
            data=[]
            other=[]
            return Response({"data": data, "sucess":False, "message":str(e), "other": other})                
         

# get conversatios
class GetConversations(APIView):
    def get(self, request):
        try:
            data={}
            path = request.build_absolute_uri('/')
            other = [{"base_image_path":path}]
            
            data=Conversation.objects.using('chat')
            
            message = "Conversations"
            return Response({"data": data, "sucess":True, "message":message, "other": other})
        except Exception as e:
            data=[]
            other=[]
            return Response({"data": data, "sucess":False, "message":str(e), "other": other}) 