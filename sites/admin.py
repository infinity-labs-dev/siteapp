from django.contrib import admin
from .models.sites import Sites
from tasks.models.tasks import Tasks
from projects.models.projects import Projects
from .models.sitetaskmapper import SiteTaskMapper
from projects.models.projecttasks import ProjectTasks

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
        
# Register your SITE models here.
admin.site.register(Sites, AdminSites)
