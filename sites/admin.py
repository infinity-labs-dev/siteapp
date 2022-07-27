from django.contrib import admin

from tasks.models.tasks import Tasks

from .models.sitetasksummary import SiteTaskSummary
from .models.sites import Sites
from .models.sitetaskmapper import SiteTaskMapper
from projects.models.projecttasks import ProjectTasks
from tasks.models.tasks import Tasks
from django.utils.html import format_html
from push_notifications.models import GCMDevice
import requests
import json
from django.conf import settings

class TaskInline(admin.TabularInline):
    model = SiteTaskMapper
    extra = 0
    fields = ['tasks', 'status', 'site_engineer', 'sequence_no', 'resource_flag', 'file', 'created_at']
    
class AdminSites(admin.ModelAdmin):
    
    list_display = ['project_id', 'site_name', 'site_type', 'spoc_name', 'spoc_contact', 'scheduled_date', 'completed_date', 'verification_status']
    fields = ('project_id', 'site_name', 'site_type', 'spoc_name', 'spoc_contact', 'site_engineer', 'address', 'latitude', 'longitude', 'scheduled_date', 'completed_date', 'verification_status')
    filter_horizontal = ['site_engineer', ]
    inlines = [TaskInline,]
    
    def save_model(self, request, obj, form, change):
        # print("POST ===", request.POST)
        # print("site_engineer", request.POST["site_engineer"])        
        obj.save()
        
        site_id = obj.id
        project_id = request.POST['project_id']
        
        tasks = ProjectTasks.objects.raw('SELECT * FROM projects_projecttasks_tasks WHERE projecttasks_id ='+ project_id)
        print("tasks", tasks)
        for e in tasks:
            SiteTaskMapper.objects.update_or_create(
                projects_id=project_id,
                sites_id=site_id,
                tasks_id=e.tasks_id,
                status="PENDING",
                created_by_id=1
            )
        pushResponse = send_push_notification(request.POST["site_engineer"], site_id)        
        print("pushResponse ==", pushResponse)                
        obj.save() 
            
def send_push_notification(user,fault):
    try:
        device = GCMDevice.objects.get(user=user)
        # print("device ===", device)
        if device:
            # site details
            site_details = Sites.objects.get(id=fault)
            if site_details:
                siteD = site_details.site_name
            else:
                 siteD = "New Site"   
            
            deviceToken=device.registration_id
            serverToken = settings.PUSH_NOTIFICATIONS_SETTINGS['FCM_API_KEY']
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=' + serverToken,
                }
            body = {
                    'data': {'title': 'Site Assigned',
                                        'body': str(siteD)+' assigned to you.'
                                        },
                    'to':
                        deviceToken,
                    'priority': 'high',
                    #   'data': dataPayLoad,
                    }


            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
            # check what is the response
            # print(response)
            
            return response
    except Exception as e:
        print(e) 

class AdminSiteTaskSummary(admin.ModelAdmin): 
    list_display =['id', 'sites', 'site_task', 'site_engineer', 'status','created_at', 'track_user', 'tracking_summary']

    def site_task(self,instance):
        task_mapper_id_id = instance.task_mapper_id_id
        mapperObject = SiteTaskMapper.objects.get(id=task_mapper_id_id)
        taskObject = Tasks.objects.get(id=mapperObject.tasks_id)
        return taskObject.task_name        

    def track_user(self,instance):
        # print('instance.task_mapper_id_id ==', instance.task_mapper_id_id)
        task_mapper_id_id=instance.task_mapper_id_id
        return format_html(f'''<a href='/resource_tracking/track_user/?ticket_id={task_mapper_id_id}' style="padding: 5px ;" target="_blank" rel="noopener noreferrer">View<a/>''')
    
    def tracking_summary(self, instance):
        # ticket_id=(instance)
        task_mapper_id_id = instance.task_mapper_id_id
        return format_html(f'''<a href='/resource_tracking/track_summary/?ticket_id={task_mapper_id_id}' style="padding: 5px ;" target="_blank" rel="noopener noreferrer">View<a/>''')

# Register your SITE models here.
admin.site.register(Sites, AdminSites)
admin.site.register(SiteTaskSummary, AdminSiteTaskSummary)
