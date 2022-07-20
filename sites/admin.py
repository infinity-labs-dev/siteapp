from django.contrib import admin

from tasks.models.tasks import Tasks

from .models.sitetasksummary import SiteTaskSummary
from .models.sites import Sites
from .models.sitetaskmapper import SiteTaskMapper
from projects.models.projecttasks import ProjectTasks
from tasks.models.tasks import Tasks
from django.utils.html import format_html

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
        obj.save()
        
        site_id = obj.id
        project_id = request.POST['project_id']
        
        tasks = ProjectTasks.objects.raw('SELECT * FROM projects_projecttasks_tasks WHERE projecttasks_id ='+ project_id)
        print("tasks", tasks)
        for e in tasks:
            # print("e.projecttasks_id ==", e.projecttasks_id)
            SiteTaskMapper.objects.update_or_create(
                projects_id=project_id,
                sites_id=site_id,
                tasks_id=e.tasks_id,
                status="PENDING",
                created_by_id=1
            )
        obj.save()     

class AdminSiteTaskSummary(admin.ModelAdmin): 
    list_display =['sites', 'site_task', 'site_engineer', 'status','created_at', 'track_user', 'tracking_summary']

    def site_task(self,instance):
        task_mapper_id_id = instance.task_mapper_id_id
        mapperObject = SiteTaskMapper.objects.get(id=task_mapper_id_id)
        taskObject = Tasks.objects.get(id=mapperObject.tasks_id)
        return taskObject.task_name        

    def track_user(self,instance):
        ticket_id=(instance)
        return format_html(f'''<a href='/resource_tracking/track_user/?ticket_id={ticket_id}' style="padding: 5px ;" target="_blank" rel="noopener noreferrer">View<a/>''')
    
    def tracking_summary(self, instance):
        ticket_id=(instance)
        return format_html(f'''<a href='/resource_tracking/track_summary/?ticket_id={ticket_id}' style="padding: 5px ;" target="_blank" rel="noopener noreferrer">View<a/>''')

# Register your SITE models here.
admin.site.register(Sites, AdminSites)
admin.site.register(SiteTaskSummary, AdminSiteTaskSummary)
