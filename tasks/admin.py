from django.contrib import admin
from tasks.models.tasks import Tasks

class AdminTasks(admin.ModelAdmin):
    list_display = ['task_name', 'description', 'status']
    list_display = ['task_name', 'description', 'status', 'created_by']
    
# Register your TASK models here.
admin.site.register(Tasks, AdminTasks)