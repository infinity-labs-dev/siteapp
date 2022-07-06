from resource_tracking.models.site_tracking import SiteTracking

def saveSiteTracking(paramsArray):
    sitetrack1 = SiteTracking()
    sitetrack1.ticket_id = paramsArray['fault_id']
    sitetrack1.latitude = paramsArray['latitude']
    sitetrack1.longitude = paramsArray['longitude']
    sitetrack1.created_by_id = paramsArray['user_id']
    sitetrack1.modified_by_id = paramsArray['user_id']
    sitetrack1.distance = paramsArray['distancekm']
    sitetrack1.status = paramsArray['status']
    sitetrack1.address=paramsArray['address']
    sitetrack1.total_time=paramsArray['total_time']
    sitetrack1.save()
    
    return sitetrack1