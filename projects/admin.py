from django.contrib import admin
from projects.models.projects import Projects
from projects.models.projecttasks import ProjectTasks

class AdminProjects(admin.ModelAdmin):
    list_display = ['project_id', 'project_name', 'project_details']
    list_display = ['project_id', 'project_name', 'project_details', 'created_by']

class AdminProjectTasks(admin.ModelAdmin):
    list_display = ['project_id', 'priority', 'status']
    filter_horizontal = ['tasks']
        
# Register your PROJECT models here.
admin.site.register(Projects, AdminProjects) 
admin.site.register(ProjectTasks, AdminProjectTasks)