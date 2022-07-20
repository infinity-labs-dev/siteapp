from resource_tracking.view import login_details,my_fault,site_details,get_faultlist_by_status,set_push_token,set_return_home ,userTracking



from django.urls import path

app_name = 'resource_tracking'

urlpatterns = [
    
    path('login_details/', login_details.GetLoginDetails.as_view(),name='get-login_details'),
    path('my_fault/', my_fault.MyFault.as_view(),name='get-fault_details'),
    path('view_my_fault/', my_fault.MyFaultView.as_view(),name='view-fault_details'),
    path('update_my_fault/', my_fault.UpdateMyFaultStatus.as_view(),name='update-fault_details'),
    path('get_site_details/', site_details.GetSiteDetails.as_view(),name='get_site_details'),
    path('get_faultlist_by_status', get_faultlist_by_status.GetFaultListByStatus.as_view(),name="get faultlist by status"),
    path('resolve_my_fault/', my_fault.ResolvedMyFaultStatus.as_view(),name='resolve my fault'),    
    path('set_push_token/', set_push_token.SetPushToken.as_view(),name='set_push_notification'),
    path('set_return_home/', set_return_home.SetReturnHome.as_view(),name='set_return_home'),
    path('track_user/', userTracking.UserTracking.as_view(),name='track_user'),
    path('track_summary/', userTracking.TrackSummary.as_view(),name='track_summary'),
    path('update_task_details/', my_fault.UpdateTaskDetails.as_view(),name='update_task_details'),
    path('get_task_details/', my_fault.viewTaskDetails.as_view(),name='get_task_details'),
    path('getAllTaskStatus/',my_fault.GetAllTaskStatus.as_view(),name='getAllTaskStatus'),
    path('update_task_tracking_status', my_fault.UpdateMySiteTaskStatus.as_view(),name="update_task_tracking_status")
]
